import gensim

import numpy as np

class Model:
    def __init__(self, messages, tokenizer):
        self.tokenizer = tokenizer
        self.innerModel = self.trainNewModel(messages)
        self.index2wordSet = set(self.innerModel.index2word)

    def trainNewModel(self, messages):
        return gensim.models.Word2Vec(
            [self.tokenizer.stemAndTokenize(message) for message in messages],
            min_count = 1)

    def __getitem__(self, index):
        return self.innerModel[index]

    def calculateSimilarity(self, messageA, messageB, indexDistance):
        fullTokensA = self.tokenizer.stemAndTokenize(messageA)
        fullTokensB = self.tokenizer.stemAndTokenize(messageB)

        width = 10
        startA = 0
        best = (float('inf'), 0) # orthogonal
        decay = (0.993 ** indexDistance) # must be related to the cosine threshold
        while startA < len(fullTokensA):
            startB = 0
            tokensA = fullTokensA[startA:(startA + width)]
            while startB < len(fullTokensB):
                tokensB = fullTokensB[startB:(startB + width)]
                cosine = self.innerModel.n_similarity(tokensA, tokensB) * decay
                centroid = self.centroidDistance(tokensA, tokensB) / decay
                pair = (centroid, cosine)
                if best is None or best > pair:
                    best = pair
                startB = startB + width / 2
            startA = startA + width / 2
        return best

    def centroidDistance(self, tokensA, tokensB):
        centroidA = sum([self[t] for t in tokensA]) / len(tokensA)
        centroidB = sum([self[t] for t in tokensB]) / len(tokensB)
        return np.linalg.norm(self.centroid(tokensA) - self.centroid(tokensB))

    def centroid(self, tokens):
        return sum([self[t] for t in tokens]) / len(tokens)

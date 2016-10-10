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

    def calculateSimilarity(self, messageA, messageB):
        tokensA = self.tokenizer.stemAndTokenize(messageA)
        tokensB = self.tokenizer.stemAndTokenize(messageB)
        if (len(tokensA) == 0 or len(tokensB) == 0):
            return (1e30, 0) # orthogonal
        cosine = self.innerModel.n_similarity(tokensA, tokensB)
        centroid = self.centroidDistance(tokensA, tokensB)
        return (centroid, cosine)

    def centroidDistance(self, tokensA, tokensB):
        centroidA = sum([self[t] for t in tokensA]) / len(tokensA)
        centroidB = sum([self[t] for t in tokensB]) / len(tokensB)
        return np.linalg.norm(self.centroid(tokensA) - self.centroid(tokensB))

    def centroid(self, tokens):
        return sum([self[t] for t in tokens]) / len(tokens)

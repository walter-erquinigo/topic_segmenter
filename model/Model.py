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
        movers = self.moversDistance(tokensA, tokensB)
        return (movers, cosine)

    def moversDistance(self, tokensA, tokensB):
        movers = self.wordEuclidDistance(tokensA[0], tokensB[0])
        for tokenA in tokensA:
            for tokenB in tokensB:
                movers = min(movers, self.wordEuclidDistance(tokenA, tokenB))
        return movers

    def wordEuclidDistance(self, tokenA, tokenB):
        return np.linalg.norm(self[tokenA] - self[tokenB])

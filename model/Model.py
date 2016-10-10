import gensim

import numpy as np

class Model:
    def __init__(self, messages):
        self.innerModel = self.trainNewModel(messages)
        self.index2wordSet = set(self.innerModel.index2word)

    def trainNewModel(self, messages):
        return gensim.models.Word2Vec(
            [message.getVectorText() for message in messages],
            min_count = 1)

    def __getitem__(self, index):
        return self.innerModel[index]

    def calculateSimilarity(self, messageA, messageB):
        return self.innerModel.n_similarity(messageA.getVectorText(), messageB.getVectorText())

import gensim
import sys
from Model import Model

INF = 1e30

class SimilarTopicCalculator:
    def __init__(self, window, messages, tokenizer):
        self.window = window
        self.model = Model(messages, tokenizer)

    def calculate(self, message):
        bestTopic = None
        for topic in self.window.getTopics():
            for topic_message in topic.getMessages():
                (centroid, cosine)= self.model.calculateSimilarity(message, topic_message)
                # roud up to 10
                centroid = int(centroid * 10) / 10.
                features = (-centroid, cosine, topic)
                if bestTopic is None or bestTopic <  features:
                    bestTopic = features

        if bestTopic is None:
            sys.exit("The window is empty")
        return TopicSimilarity(bestTopic[2], bestTopic[1])

class TopicSimilarity:
    def __init__(self, topic, score):
        self.topic = topic
        self.score = score

    def getTopic(self):
        return self.topic

    def getScore(self):
        return self.score

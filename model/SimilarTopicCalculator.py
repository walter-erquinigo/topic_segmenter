import gensim
import sys
from Model import Model

INF = 10000000

class SimilarTopicCalculator:
    def __init__(self, window, messages):
        self.window = window
        self.model = Model(messages)

    def calculate(self, message):
        best_topic = (-INF, None)
        for topic in self.window.getTopics():
            similarity = self.model.calculateSimilarity(topic.getStartMessage(), message)
            best_topic = max(best_topic, (similarity, topic))

        if best_topic[0] == -INF:
            sys.exit("The window is empty")
        return TopicSimilarity(best_topic[1], best_topic[1])

class TopicSimilarity:
    def __init__(self, topic, score):
        self.topic = topic
        self.score = score

    def getTopic(self):
        return self.topic

    def getScore(self):
        return self.score

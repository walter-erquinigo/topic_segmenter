import gensim
import sys
import math
from Model import Model

class SimilarTopicCalculator:
    def __init__(self, window, messages, tokenizer):
        self.window = window
        self.model = Model(messages, tokenizer)

    def calculate(self, message):
        similarities = []
        for topic in self.window.getTopics():
            for topic_message in topic.getMessages():
                (centroidDistance, cosine) = self.model.calculateSimilarity(
                    message, topic_message, message.getID() - topic_message.getID())
                similarities.append(TopicSimilarity(topic, cosine, centroidDistance))
        similarities.sort(key=lambda x: x.getCentroidDistance())
        # get top 5 percent
        size = int(math.ceil(len(similarities) * 5. / 100))
        similarities = similarities[0:size]
        similarities.sort(key= lambda x: -x.getScore())
        return None if len(similarities) == 0 else similarities[0]

class TopicSimilarity:
    def __init__(self, topic, score, centroidDistance):
        self.topic = topic
        self.score = score
        self.centroidDistance = centroidDistance

    def getTopic(self):
        return self.topic

    def getScore(self):
        return self.score

    def getCentroidDistance(self):
        return self.centroidDistance

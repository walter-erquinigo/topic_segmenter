from collections import deque

class Window:
    def __init__(self, window_size):
        self.topics = []
        self.windowSize = window_size

    def addTopic(self, topic):
        self.topics.append(topic)
        if len(self.topics) == self.windowSize + 1:
            self.topics = self.topics[1:-1]

    def getTopics(self):
        return self.topics

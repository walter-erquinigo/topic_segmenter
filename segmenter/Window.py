from collections import deque

class Window:
    def __init__(self, window_size):
        self.topics = []
        self.windowSize = window_size

    def addTopic(self, topic):
        if topic in self.topics:
            index = self.topics.index(topic)
            self.topics[index], self.topics[-1] = self.topics[-1], self.topics[index]
        else:
            self.topics.append(topic)
            if len(self.topics) == self.windowSize + 1:
                self.topics = self.topics[1:]

    def getTopics(self):
        return self.topics

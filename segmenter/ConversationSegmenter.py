from Window import Window
from model.SimilarTopicCalculator import SimilarTopicCalculator
from model.ReplyObjectPredictor import ReplyObjectPredictor
from text.Topic import Topic

class ConversationSegmenter:
    def __init__(self, messages, windowSize, alpha):
        self.messages = messages
        self.window = Window(windowSize)
        self.similarTopicCalculator = SimilarTopicCalculator(self.window, messages)
        self.replyObjectPredictor = ReplyObjectPredictor(
            self.window, alpha, self.similarTopicCalculator)

    def segment(self):
        topics = [None for i in self.messages]
        topicSet = []
        for i, message in enumerate(self.messages):
            if i > 0 and self.messages[i - 1].getAuthor() == message.getAuthor():
                topics[i] = topics[i - 1]
            else:
                replied_topic = self.replyObjectPredictor.predict(message)
                if replied_topic is None:
                    topic = Topic(message)
                    topicSet.append(topic)
                    self.window.addTopic(topic)
                else:
                    topic = replied_topic
                topics[i] = topic
            topics[i].appendMessage(message)
        return topicSet

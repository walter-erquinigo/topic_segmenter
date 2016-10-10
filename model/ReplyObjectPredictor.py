import nltk

from grammar.SentenceGrammarAnalyzer import SentenceGrammarAnalyzer

class ReplyObjectPredictor:
    def __init__(self, window, alpha, similar_topic_calculator):
        self.window = window
        self.alpha = alpha
        self.similarTopicCalculator = similar_topic_calculator

    def predict(self, message):
        if len(self.window.getTopics()) == 0:
            return None
        similarity = self.similarTopicCalculator.calculate(message)
        best_topic = None
        analyzer = SentenceGrammarAnalyzer(message)
        if analyzer.isAReply() or similarity.getScore() >= self.alpha:
            best_topic = similarity.getTopic()
        return best_topic

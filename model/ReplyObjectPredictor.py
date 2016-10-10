import nltk

from grammar.SentenceGrammarAnalyzer import SentenceGrammarAnalyzer

class ReplyObjectPredictor:
    def __init__(self, window, alpha, similar_topic_calculator, tokenizer):
        self.window = window
        self.alpha = alpha
        self.similarTopicCalculator = similar_topic_calculator
        self.tokenizer = tokenizer

    def predict(self, message):
        if len(self.window.getTopics()) == 0:
            return None
        similarity = self.similarTopicCalculator.calculate(message)
        best_topic = None
        analyzer = SentenceGrammarAnalyzer(message, self.tokenizer)
        if analyzer.isAReply() or similarity.getScore() >= self.alpha:
            best_topic = similarity.getTopic()
        return best_topic

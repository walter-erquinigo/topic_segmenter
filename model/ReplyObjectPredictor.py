import nltk

from grammar.SentenceGrammarAnalyzer import SentenceGrammarAnalyzer

class ReplyObjectPredictor:
    def __init__(self, window, cosineSimilarityThreshold, similar_topic_calculator, tokenizer):
        self.window = window
        self.cosineSimilarityThreshold = cosineSimilarityThreshold
        self.similarTopicCalculator = similar_topic_calculator
        self.tokenizer = tokenizer

    def predict(self, message):
        if len(self.window.getTopics()) == 0:
            return (None, 'window empty')
        similarity = self.similarTopicCalculator.calculate(message)
        best_topic = (None, 'no similarity nor grammatically a reply')
        analyzer = SentenceGrammarAnalyzer(message, self.tokenizer)
        (isReply, reason) = analyzer.isAReply()
        if isReply:
            best_topic = (similarity.getTopic(), 'grammatically ' + reason)
        elif similarity.getScore() >= self.cosineSimilarityThreshold:
            best_topic = (similarity.getTopic(), 'cosine ' + str(similarity.getScore()))
        elif self.window.getTopics()[-1].size() == 1:
            best_topic = (self.window.getTopics()[-1], 'previous topic with one element')
        return best_topic

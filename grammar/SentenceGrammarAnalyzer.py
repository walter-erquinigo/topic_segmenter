import nltk
from sets import Set

class SentenceGrammarAnalyzer:
    REPLY_POS_VALID_UNIVERSAL_TAGS = Set(['CONJ'])
    # check http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html for
    # a good list
    REPLY_POS_VALID_UPENN_TAGS = Set(['WDT', 'DT'])
    REPLY_STARTERS = Set(['ok', 'ok.', 'k', 'k.' 'mine', 'his', 'hers', 'theirs', 'ours'])

    def __init__(self, message, tokenizer):
        self.message = message
        self.tokenizer = tokenizer

    def isAReply(self):
        stemmedTokens = self.tokenizer.stemAndTokenize(self.message)

        if len(stemmedTokens) <= 1:
            return (True, 'stemmed length of ' + str(len(stemmedTokens)))

        tokens = self.tokenizer.tokenize(self.message)
        univeralTags = nltk.pos_tag(tokens, tagset='universal')

        if univeralTags[0][1] in SentenceGrammarAnalyzer.REPLY_POS_VALID_UNIVERSAL_TAGS:
            return (True, 'universal tag ' + univeralTags[0][1])

        upennTags = nltk.pos_tag(tokens)
        if upennTags[0][1] in SentenceGrammarAnalyzer.REPLY_POS_VALID_UPENN_TAGS:
            return (True, 'upenn tag ' + upennTags[0][1])
        if tokens[0].lower() in SentenceGrammarAnalyzer.REPLY_STARTERS:
            return (True, 'reply starter ' + tokens[0].lower())
        return (False, 'not a reply')

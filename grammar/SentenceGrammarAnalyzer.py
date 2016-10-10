import nltk
from sets import Set

class SentenceGrammarAnalyzer:
    REPLY_POS_VALID_UNIVERSAL_TAGS = Set(['CONJ', 'ADJ', 'ADV'])
    # check http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html for
    # a good list
    REPLY_POS_VALID_UPENN_TAGS = Set(['PRP$'])

    def __init__(self, message, tokenizer):
        self.message = message
        self.tokenizer = tokenizer

    def isAReply(self):
        univeralTags = nltk.pos_tag(
            self.tokenizer.stemAndTokenize(self.message), tagset='universal')
        if (univeralTags[0][1] in SentenceGrammarAnalyzer.REPLY_POS_VALID_UNIVERSAL_TAGS):
            return True

        upennTags = nltk.pos_tag(
            self.tokenizer.stemAndTokenize(self.message))
        if (upennTags[0][1] in SentenceGrammarAnalyzer.REPLY_POS_VALID_UPENN_TAGS):
            return True

        return False

from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
from nltk.corpus import stopwords
import re

class MessageTokenizer:
    def __init__(self):
        self.stopWords = []#stopwords.words("english")
        self.stemmer = SnowballStemmer('english')
        self.cache = {}
        self.userRe = re.compile('<@U\w\w\w\w\w\w\w\w>')

    def stemAndTokenize(self, message):
        id = message.getID()
        if (id not in self.cache.keys()):
            self.cache[id] = [self.stemmer.stem(t) for t in self.getValidTokens(message)]
        return self.cache[id]

    def tokenize(self, message):
        return [w for w in word_tokenize(self.removeUsers(message))]

    def punctuationTokenize(self, message):
        return [w for w in self.tokenize(message) if w.isalnum()]

    def getValidTokens(self, message):
        return [word for word in self.punctuationTokenize(message)
            if word not in self.stopWords]

    def removeUsers(self, message):
        return self.userRe.sub('', message.getText())

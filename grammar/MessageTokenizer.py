from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
from nltk.corpus import stopwords

class MessageTokenizer:
    def __init__(self):
        self.stopWords = stopwords.words("english")
        self.stemmer = SnowballStemmer('english')
        self.cache = {}

    def stemAndTokenize(self, message):
        id = message.getID()
        if (id not in self.cache.keys()):
            self.cache[id] = [self.stemmer.stem(t) for t in self.getValidTokens(message)]
        return self.cache[id]

    def getValidTokens(self, message):
        return [word for word in word_tokenize(message.getText())
            if word not in self.stopWords]

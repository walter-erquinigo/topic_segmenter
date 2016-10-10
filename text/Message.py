from nltk import word_tokenize
import numpy as np

class Message:
    def __init__(self, text, author):
        self.text = text
        self.vectorText = word_tokenize(text)
        self.author = author

    def getVectorText(self):
        return self.vectorText

    def getAuthor(self):
        return self.author

    def getText(self):
        return self.text

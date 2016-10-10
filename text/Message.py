import numpy as np


class Message:
    def __init__(self, id, text, author):
        self.id = id
        self.text = text
        self.vectorText = None
        self.author = author

    def getAuthor(self):
        return self.author

    def getText(self):
        return self.text

    def getID(self):
        return self.id

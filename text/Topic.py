class Topic:
    def __init__(self, startMessage):
        self.startMessage = startMessage
        self.messages = []

    def appendMessage(self, message):
        self.messages.append(message)

    def getMessages(self):
        return self.messages

    def getStartMessage(self):
        return self.startMessage

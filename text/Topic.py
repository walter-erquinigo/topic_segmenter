class Topic:
    def __init__(self, startMessage, reason):
        self.startMessage = startMessage
        self.messages = [startMessage]
        self.reasons = [reason]

    def appendMessage(self, message, reason):
        self.messages.append(message)
        self.reasons.append(reason)

    def getMessages(self):
        return self.messages

    def getReasons(self):
        return self.reasons

    def getStartMessage(self):
        return self.startMessage

    def size(self):
        return len(self.messages)

    def absorve(self, other):
        self.messages = self.messages + other.messages
        self.messages.sort(key=lambda x: x.getID())
        self.reasons.extend( other.reasons )  # append reasons from other topic

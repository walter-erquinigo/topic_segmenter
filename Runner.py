import sys

from text.Message import Message
from grammar.MessageTokenizer import MessageTokenizer
from segmenter.ConversationSegmenter import ConversationSegmenter
from text.JSONParser import JSONParser

class TestRunner:
    def __init__(self, json_file_name):
        self.jsonFileName = json_file_name

    def run(self):
        parser = JSONParser(self.jsonFileName)
        self.messages = parser.getMessages()
        self.tokenizer = MessageTokenizer()
        segmenter = ConversationSegmenter(self.messages, 3, 0.2, self.tokenizer)
        topics = segmenter.segment()
        self.report(topics)

    def report(self, topics):
        idGroups = []
        for topic in topics:
            print("== Topic ==")
            idGroup = []
            for message in topic.getMessages():
                idGroup.append(message.getID())
                print("\t" + message.getText())
                print("\t\t" + str(self.tokenizer.stemAndTokenize(message)))
            print("\n")
            idGroups.append(idGroup)

        print("===============================")
        print(idGroups)


def main(json_input):
    TestRunner(json_input).run()

if __name__ == '__main__':
    main(sys.argv[1])

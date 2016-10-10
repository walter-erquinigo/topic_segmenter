import sys

from text.Message import Message
from segmenter.ConversationSegmenter import ConversationSegmenter
from text.JSONParser import JSONParser

class TestRunner:
    def __init__(self, json_file_name):
        parser = JSONParser(json_file_name)
        self.messages = parser.getMessages()

    def run(self):
        segmenter = ConversationSegmenter(self.messages, 3, 0.2)
        topics = segmenter.segment()
        self.report(topics)

    def report(self, topics):
        for topic in topics:
            print("== Topic ==")
            for message in topic.getMessages():
                print("\t-- Message --")
                print("\t" + message.getText())
            print("\n")


def main(json_input):
    TestRunner(json_input).run()

if __name__ == '__main__':
    main(sys.argv[1])

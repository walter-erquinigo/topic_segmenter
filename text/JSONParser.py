from pprint import pprint
import json
from Message import Message

USER = u'user'
ANON_TEXT = u'anon_text'

class JSONParser:
    def __init__(self, file_name):
        self.file_name = file_name
        self.jsonObject = self.parse()

    def parse(self):
        with open(self.file_name) as data_file:
            return json.load(data_file)

    def getMessages(self):
        users = self.jsonObject[USER]
        texts = self.jsonObject[ANON_TEXT]
        return sorted(
            [Message(int(id), texts[id], users[id]) for id in users.keys()],
            key=lambda message: message.getID())

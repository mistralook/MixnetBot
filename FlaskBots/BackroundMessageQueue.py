from FlaskBots.Network import get_all_servers
import random
import json
import requests
import time
from Protocol.FieldType import Field


class Message:
    def __init__(self, url: str, data: dict):
        self.url = url
        if not isinstance(data, dict):
            raise TypeError
        self.data = data

    def send(self):
        requests.post(url=self.url, json=self.data)


class MessageQueue:
    def __init__(self):
        self.messages = list()
        self.send_interval = 5
        self.buffer_size = 10
        self.bm = """{
                "body": {
                    "body": {
                        "body": "Hi",
                        "to": "None",
                        "sender_pub_k": "111",
                        "cypher_count": 0
                    },
                    "to_pub_k": "somepk",
                    "to": "recipient Mark",
                    "cypher_count": 1
                },
                "to": "tototo",
                "cypher_count": 2
            }"""

    def fill_by_junk(self):
        servers = get_all_servers()
        if len(self.messages) < self.buffer_size:
            for i in range(self.buffer_size - len(self.messages)):
                mes = json.loads(self.bm)
                junk_mes = {Field.to: None,
                            Field.body: "J" * random.randrange(0, 100)}
                receiver = servers[random.randrange(0, len(servers))] + "/message"
                self.append_message(Message(url=receiver, data=junk_mes))

    def send_mixed(self):
        while True:
            time.sleep(self.send_interval)
            self.fill_by_junk()
            random.shuffle(self.messages)
            for message in self.messages:
                message.send()
            self.messages.clear()

    def append_message(self, mes: Message):
        self.messages.append(mes)

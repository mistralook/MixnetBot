import json
import sys

import requests

from Keys import get_keys
from db.MailRepository import MailRepository

sys.path.append('../')
from Protocol.FieldType import Field
from multiple_encryption import multiple_encrypt
from FlaskBots.Network import get_all_servers

mail_repo = MailRepository()


def build_route(recv_pub_k):
    return get_all_servers() + [recv_pub_k]


def send(recv_pub_k, message: str):
    route = build_route(recv_pub_k)
    onion_encrypted = multiple_encrypt(message, route)
    first_node = onion_encrypted[Field.to]
    dumped = json.dumps(onion_encrypted)
    requests.post(url=first_node, json=dumped)
    print(dumped)
    print("sent")


def save_updates():
    server = get_all_servers()[0]
    pub_k = get_keys()["public_key"]
    response = requests.get(url=f"{server}/messages", json=json.dumps({"sender_public_key": pub_k}))
    messages = response.json()["messages"]
    messages = list(map(lambda m: json.loads(m)[Field.body], messages))
    # print(messages[0])
    # print(type(messages[0]))
    save_messages(messages)
    # return messages
    # return [json.loads(m)[Field.body][Field.body] for m in messages]


def save_messages(messages):
    for m in messages:
        mail_repo.add_message(m[Field.sender_pub_k], m[Field.body])


def get_messages_by_pub_k(sender_pub_k):
    return [m.text for m in mail_repo.get_messages_by_sender_pub_k(sender_pub_k)]

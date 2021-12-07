import json
import sys

import requests

from Keys import get_keys
from db.MailRepository import MailRepository
from utils.coding import base64_str_to_public_key

sys.path.append('../')
from Protocol.FieldType import Field
from multiple_encryption import multiple_encrypt
from FlaskBots.Network import get_all_servers

mail_repo = MailRepository()


def build_route(recv_pub_k):
    return get_all_servers() + [recv_pub_k]


# def get_pub_keys():
#     pub_key_by_mixer_addr = {}  # key - addr, value - PubKey(from pyNacl)
#     for mixer in get_all_servers():
#         response = requests.get(f"{mixer}/public-key")
#         pub_key = base64_str_to_public_key(response.json()['public_key'])
#         pub_key_by_mixer_addr[mixer] = pub_key
#     return pub_key_by_mixer_addr


def send(recv_pub_k, message: str):
    route = build_route(recv_pub_k)
    onion_encrypted = multiple_encrypt(message, route)
    first_node = onion_encrypted[Field.to]
    data = onion_encrypted[Field.body]
    print("sent", data)
    requests.post(url=first_node, data=data)


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

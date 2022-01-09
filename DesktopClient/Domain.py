import json
import sys

import requests

from Keys import get_keys, get_keys_f
from Protocol.UpdateRequest import UpdateReq
from db.MailRepository import MailRepository
from utils.coding import base64_str_to_public_key, unpack_obj, pack_k, pack_obj

sys.path.append('../')
from Protocol.FieldType import Field
from multiple_encryption import multiple_encrypt, get_pub_keys
from FlaskBots.Network import get_all_servers

mail_repo = MailRepository()


def build_route(recv_pub_k):
    return 1 * get_all_servers() + [recv_pub_k]


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


def get_updates():
    server = get_all_servers()[0]
    server_pub_k = get_pub_keys()[server]  # TODO доставать из локального хранилища
    keys = get_keys_f()
    message = get_update_request_message()
    response = requests.get(url=f"{server}/messages", data=pack_obj(message, server_pub_k))
    d = unpack_obj(data=response.text, sk=keys.private_key)
    senders = set()
    messages = []
    for m in d["messages"]:
        encrypted = json.loads(m)
        unp = unpack_obj(encrypted[Field.body], keys.private_key)
        mail_repo.add_message(unp[Field.sender_pub_k], unp[Field.body], unp[Field.timestamp],
                              unp[Field.uid])
        senders.add(unp[Field.sender_pub_k])
        messages.append(unp[Field.body])
    return senders, messages


def get_update_request_message():
    keys = get_keys_f()
    return {UpdateReq.sender_public_key: pack_k(keys.public_key),
            UpdateReq.last_message_time: mail_repo.get_last_message_time(),
            UpdateReq.all_message_hash: mail_repo.get_all_messages_hash()}


def get_messages_by_pub_k(sender_pub_k):
    return [m.text for m in mail_repo.get_messages_by_sender_pub_k(sender_pub_k)]

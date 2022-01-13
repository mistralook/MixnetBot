import json
import random
import sys
import time

import requests

from FlaskBots.ConnectionManager import ConnectionManager
from Keys import get_keys_f
from Protocol.UpdateRequest import UpdateReq
from db.MailRepository import MailRepository
from utils.coding import base64_str_to_public_key, unpack_obj, pack_k, pack_obj, unpack_str, unpack_pub_k

sys.path.append('../')
from Protocol.FieldType import Field
from multiple_encryption import multiple_encrypt, get_pub_keys
from FlaskBots.Network import get_all_servers

mail_repo = MailRepository()
conn_manager = ConnectionManager(False).start()
time.sleep(2)
keys = get_keys_f()


def build_route(recv_pub_k):
    return [s.addr for s in conn_manager.get_online_servers()] + [recv_pub_k]


def send(recv_pub_k, message: str):
    route = build_route(recv_pub_k)
    onion_encrypted = multiple_encrypt(message, route, conn_manager)
    first_node = onion_encrypted[Field.to]
    data = onion_encrypted[Field.body]
    print("sent", data)
    requests.post(url=first_node, data=data)
    return conn_manager  # TODO DELETE


def get_updates():
    server = random.choice(conn_manager.get_online_servers())

    upd_request = get_update_request_message()
    try:
        response = requests.get(url=f"{server.addr}/messages", data=pack_obj(upd_request, server.pub_k))
        return parse_updates(response)
    except requests.exceptions.RequestException:
        return [], []


def parse_updates(response):
    try:
        d = unpack_obj(data=response.text, sk=keys.private_key)
    except:
        raise Exception(response.text)
    senders = set()
    messages = []
    for m in d["messages"]:
        encrypted = json.loads(m)
        unp = unpack_obj(encrypted[Field.body], keys.private_key)
        sender_pub_k = unpack_pub_k(unp[Field.sender_pub_k])
        # TODO Если упало с ошибкой, то сообщение - подделка
        mes = unpack_str(unp[Field.body], keys.private_key, sender_pub_k)
        mail_repo.add_message(unp[Field.sender_pub_k], mes, unp[Field.timestamp],
                              unp[Field.uid])
        senders.add(unp[Field.sender_pub_k])
        messages.append(unp[Field.body])
    return list(senders), messages


def get_update_request_message():
    return {UpdateReq.sender_public_key: pack_k(keys.public_key),
            UpdateReq.last_message_time: mail_repo.get_last_message_time(),
            UpdateReq.all_message_hash: mail_repo.get_all_messages_hash()}


def get_messages_by_pub_k(sender_pub_k):
    return [m.text for m in mail_repo.get_messages_by_sender_pub_k(sender_pub_k)]


def get_all_chats():
    return mail_repo.get_all_senders()

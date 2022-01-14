import json
import random
import sys
import time

import requests

from DesktopClient.KeyManager import KeyManager
from FlaskBots.ConnectionManager import ConnectionManager
from db.MailRepository import MailRepository
from utils.coding import base64_str_to_public_key, unpack_obj, pack_k, pack_obj, unpack_str, unpack_pub_k

sys.path.append('../')
from Protocol.FieldType import Field
from multiple_encryption import multiple_encrypt, get_pub_keys


class MixnetClient:
    def __init__(self):
        self.mail_repo = MailRepository()
        self.conn_manager = ConnectionManager(False).start()
        self.key_manager = KeyManager()
        self.key_manager.try_generate_and_save_keys(nickname="User")
        print("Client & Connection manager STARTED")
        # time.sleep(2)

    def send(self, recv_pub_k, message: str):
        route = self.build_route(recv_pub_k)
        onion_encrypted = multiple_encrypt(message, route, self.conn_manager)
        first_node = onion_encrypted[Field.to]
        data = onion_encrypted[Field.body]
        # print("sent", data)
        requests.post(url=first_node, data=data)

    def build_route(self, recv_pub_k):
        return [s.addr for s in self.conn_manager.get_online_servers()] + [recv_pub_k]

# def get_messages_by_pub_k(sender_pub_k):
#     return [m.text for m in mail_repo.get_messages_by_sender_pub_k(sender_pub_k)]
#
#
# def get_all_chats():
#     return mail_repo.get_all_senders()

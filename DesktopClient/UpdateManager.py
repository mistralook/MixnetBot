import json
import random
import sys
import time
from threading import Thread
from dateutil import parser
import requests

from DesktopClient.db.MailRepository import MessageDirection
from Protocol.UpdateRequest import UpdateReq
from utils.coding import base64_str_to_public_key, unpack_obj, pack_k, pack_obj, unpack_str, unpack_pub_k

sys.path.append('../')
from Protocol.FieldType import Field
from multiple_encryption import multiple_encrypt, get_pub_keys


class UpdateManager:
    def __init__(self, conn_manager, key_manager, repo):
        self.conn_manager = conn_manager
        self.key_manager = key_manager
        self.repo = repo

    def start(self):
        thread = Thread(target=self.get_updates, daemon=True)
        thread.start()
        # time.sleep(3)
        return self

    def get_updates(self):
        try:
            server = random.choice(self.conn_manager.get_online_servers())
        except RuntimeError:  # all offline
            return [], []
        upd_request = self.get_update_request_message()
        try:
            response = requests.get(url=f"{server.addr}/messages", data=pack_obj(upd_request, server.pub_k))
            return self.parse_updates(response)
        except requests.exceptions.RequestException:
            return [], []

    def parse_updates(self, response):
        try:
            d = unpack_obj(data=response.text, sk=self.key_manager.sk)
        except:
            return [], []
            # raise Exception(response.text)
        senders = set()
        messages = []
        for m in d["messages"]:
            encrypted = json.loads(m)
            unp = unpack_obj(encrypted[Field.body], self.key_manager.sk)
            sender_pub_k = unpack_pub_k(unp[Field.sender_pub_k])
            # TODO Если упало с ошибкой, то сообщение - подделка
            mes = unpack_str(unp[Field.body], self.key_manager.sk, sender_pub_k)
            ts = parser.parse(unp[Field.timestamp])
            self.repo.mail.add_message(unp[Field.sender_pub_k], mes, ts,
                                       unp[Field.uid], direction=MessageDirection.incoming)
            senders.add(unp[Field.sender_pub_k])
            messages.append(unp[Field.body])
        return list(senders), messages

    def get_update_request_message(self):
        return {UpdateReq.sender_public_key: pack_k(self.key_manager.pk),
                UpdateReq.last_message_time: self.repo.mail.get_last_message_time(),
                UpdateReq.all_message_hash: self.repo.mail.get_all_messages_hash()}

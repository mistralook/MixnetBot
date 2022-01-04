import argparse
import json
from threading import Thread
import requests
from flask import Flask
from flask import request
from nacl.public import PrivateKey, SealedBox

from DesktopClient.multiple_encryption import get_pub_keys
from FlaskBots.BackroundMessageQueue import MessageQueue, Message
from db.DB import DB
from db.MailRepository import MailRepository
from FlaskBots.Network import get_all_servers
from Protocol.FieldType import Field
from db.UserRepository import UserRepository
from utils.coding import bytes_to_b64, b64to_bytes, pack_k, unpack_obj, pack_obj

app = Flask(__name__)
db = DB()
message_queue = MessageQueue()

PRIVATE_KEY = PrivateKey.generate()
PUBLIC_KEY = PRIVATE_KEY.public_key
print("PUBLIC KEY", PUBLIC_KEY.__bytes__())


def get_json_dict(request) -> dict:
    data = request.get_data()
    return unpack_obj(data=data, sk=PRIVATE_KEY)


@app.route("/public-key", methods=['GET'])
def get_public_key():
    body = request.get_json()
    # print(PUBLIC_KEY)
    response = {
        "public_key": pack_k(PUBLIC_KEY),
        "private_key": pack_k(PRIVATE_KEY),
        "encoding": "base64"}
    # print(response)
    return response


@app.route("/hello", methods=['POST'])
def hi():
    body = request.get_data()
    print(body.decode())
    return "ok"


@app.route("/message-broadcast", methods=['POST'])
def message_broadcast():
    message = request.get_json()
    db.mail_repo.add_message(recv_pub_k=message[Field.to_pub_k], message=message[Field.body])
    return "OK", 200


@app.route("/message", methods=['POST'])
def message():
    message = get_json_dict(request)  # расшифрованное своим приватным ключом
    print("MES:", message)
    if message.get(Field.is_junk):
        return "OK", 200
    if message[Field.cypher_count] == 1:
        if message.get(Field.type) == "broadcast":
            db.mail_repo.add_message(recv_pub_k=message[Field.to_pub_k], message=json.dumps(message))
            print("saved", json.dumps(message))
        else:
            send_broadcast(message)
        return "OK", 200
    send_to_next_node(message)
    return "OK", 200


def send_to_next_node(message):
    message_queue.append_message(Message(url=message[Field.to], data=message[Field.body]))


def print_response(r):
    print(f"Redirected. {r.text}")


def send_broadcast(message):
    mixers_pub_keys = get_pub_keys()
    message[Field.type] = "broadcast"
    for server in get_all_servers():
        encrypted = pack_obj(message, mixers_pub_keys[server])  # Зашифровали для получателя
        message_queue.append_message(Message(url=server + "/message", data=encrypted))
    print("sent brodcast", message)


@app.route("/messages", methods=['GET'])
def get_all_messages():
    message = get_json_dict(request)
    pub_k = message[Field.sender_public_key]
    return {"messages": db.mail_repo.get_messages_by_recv_pub_k(pub_k)}


@app.route("/user", methods=['POST'])
def register_new_user():
    message_obj = get_json_dict(request)
    pub_k = message_obj[Field.sender_public_key]
    nickname = message_obj[Field.sender_nickname]
    success = db.user_repo.add_user(pub_k, nickname)
    if success:
        for server in get_all_servers():
            message_queue.append_message(Message(url=server + "/user", data=message_obj))
    return "OK", 200


if __name__ == '__main__':
    thread = Thread(target=message_queue.send_mixed)
    thread.start()
    parser = argparse.ArgumentParser()
    parser.add_argument("--xport", dest="xport", default=5000, type=int)
    args = parser.parse_args()
    db.connect(args.xport)
    app.run(port=args.xport)

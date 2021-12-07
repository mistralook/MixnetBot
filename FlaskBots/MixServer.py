import argparse
import json
from threading import Thread
import requests
from flask import Flask
from flask import request
from nacl.public import PrivateKey, SealedBox
from FlaskBots.BackroundMessageQueue import MessageQueue, Message
from db.DB import DB
from db.MailRepository import MailRepository
from FlaskBots.Network import get_all_servers
from Protocol.FieldType import Field
from db.UserRepository import UserRepository
from utils.coding import bytes_to_b64, b64to_bytes

app = Flask(__name__)
db = DB()
message_queue = MessageQueue()

PRIVATE_KEY = PrivateKey.generate()
PUBLIC_KEY = PRIVATE_KEY.public_key


def get_json_dict(request):
    print(request.get_data())
    message = request.get_data()
    print("---------------------------------------------------------------")
    print("DATA:", message)
    print("DATA TYPE:", type(message))
    box = SealedBox(PRIVATE_KEY)
    message = box.decrypt(b64to_bytes(message)).decode()
    print("##################################################################")
    print("MES:", message)
    print("MES TYPE:", type(message))

    if isinstance(message, str):
        print('000000000000000000000000000000000000000')
        print("message is str", message)
        message = json.loads(message)
    return message


@app.route("/public-key", methods=['GET'])
def get_public_key():
    body = request.get_json()
    print(PUBLIC_KEY)
    pk = bytes_to_b64(PUBLIC_KEY._public_key)
    response = {"public_key": f"{pk}",
                "encoding": "base64"}
    print(response)
    return response


@app.route("/message-broadcast", methods=['POST'])
def message_broadcast():
    message = request.get_json()
    db.mail_repo.add_message(recv_pub_k=message[Field.to_pub_k], message=message[Field.body])
    return "OK", 200


@app.route("/message", methods=['POST'])
def message():
    message = get_json_dict(request)

    if not message[Field.to]:  # received junk
        return "OK", 200
    if message[Field.cypher_count] == 1:
        if message.get(Field.type) != "broadcast":
            pass
            # send_broadcast(message)
        else:
            db.mail_repo.add_message(recv_pub_k=message[Field.to_pub_k], message=json.dumps(message))
        return "OK", 200
    send_to_next_node(message)
    return "OK", 200


def send_to_next_node(message):
    message_queue.append_message(Message(url=message[Field.to], data=message[Field.body]))


def print_response(r):
    print(f"Redirected. {r.text}")


def send_broadcast(message):
    for server in get_all_servers():
        message[Field.type] = "broadcast"

        message_queue.append_message(Message(url=server + "/message", data=message))


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

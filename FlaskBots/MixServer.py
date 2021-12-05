import argparse
import json
import random
from threading import Thread
import time
import requests
from flask import Flask
from flask import request

from db.DB import DB
from db.MailRepository import MailRepository
from FlaskBots.Network import get_all_servers
from Protocol.FieldType import Field
from db.UserRepository import UserRepository

app = Flask(__name__)
db = DB()
message_queue = MessageQueue()


def get_json_dict(request):
    message = request.get_json(force=True)
    if isinstance(message, str):
        message = json.loads(message)
    return message


@app.route("/public-key", methods=['POST'])
def get_public_key():
    body = request.get_json()
    response = {"public_key": "some_PK",
                "encoding": "base64"}
    return response


@app.route("/message", methods=['POST'])
def message():
    message = get_json_dict(request)
    if not message[Field.to]:  # received junk
        return "OK", 200
    if message[Field.cypher_count] == 1:
        if message.get(Field.type) != "broadcast":
            send_broadcast(message)
        else:
            db.mail_repo.add_message(recv_pub_k=message[Field.to_pub_k], message=json.dumps(message))

        return "OK", 200
    send_to_next_node(message)
    return "OK", 200


def send_to_next_node(message):
    messages.append({"target": requests.post, "url": message[Field.to], "json": message, "do": print_response})


def print_response(r):
    print(f"Redirected. {r.text}")


def send_broadcast(message):
    for server in get_all_servers():
        messages.append({"target": requests.post, "url": server + "/message", "json": message})


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

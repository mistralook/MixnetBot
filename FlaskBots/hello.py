import argparse
import json

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


def get_json_dict(request):
    message = request.get_json(force=True)
    if isinstance(message, str):
        message = json.loads(message)
    return message


@app.route("/hello", methods=['GET', 'POST'])
def hello_world():
    return "<p>Hello, World!</p>"


# bytes_to_b64(PUBLIC_KEY.encode())
@app.route("/public-key", methods=['POST'])
def get_public_key():
    body = request.get_json()
    response = {"public_key": "some_PK",
                "encoding": "base64"}
    return response


@app.route("/message", methods=['POST'])
def message():
    message = get_json_dict(request)
    if message[Field.cypher_count] == 1:  # т.е. прислали широковещательно
        message[Field.type] = "broadcast"
        db.mail_repo.add_message(recv_pub_k=message[Field.to_pub_k], message=json.dumps(message))
    encrypted = message[Field.body]
    decrypted = json.dumps(encrypted)  # пока так потому что дешифратор вернет строчку, а не словарь
    inner = json.loads(decrypted)  # cast str to obj
    # print(f"INNER: {inner}")
    if inner[Field.cypher_count] == 1:
        send_broadcast(inner)
    if inner[Field.cypher_count] > 1:
        send_to_next_node(inner)
    return "OK", 200


def send_to_next_node(message):
    response = requests.post(url=message[Field.to], json=message)
    print(f"Redirected. {response.text}")


def send_broadcast(message):
    # print(f"BROADCASTING: {message}")
    for server in get_all_servers():
        response = requests.post(url=server + "/message", json=message)


@app.route("/messages", methods=['GET'])
def get_all_messages():
    message = get_json_dict(request)
    pub_k = message[Field.sender_public_key]
    return {"messages": db.mail_repo.get_messages_by_recv_pub_k(pub_k)}


@app.route("/user", methods=['POST'])
def register_new_user():
    message_obj = request.get_json(force=True)
    pub_k = message_obj[Field.sender_public_key]
    nickname = message_obj[Field.sender_nickname]
    success = db.user_repo.add_user(pub_k, nickname)
    if success:
        for server in get_all_servers():
            response = requests.post(url=server + "/user", json=json.dumps(message_obj))
    return "OK", 200


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--xport", dest="xport", default=5000, type=int)
    args = parser.parse_args()
    db.connect(args.xport)
    app.run(port=args.xport)

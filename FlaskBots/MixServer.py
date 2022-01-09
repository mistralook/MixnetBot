import argparse
import json
from threading import Thread

from flask import Flask
from flask import request

from DesktopClient.multiple_encryption import get_pub_keys
from FlaskBots.BackroundMessageQueue import MessageQueue, MessageTask
from FlaskBots.Network import get_all_servers
from FlaskBots.db.DB import DB
from Protocol.FieldType import Field
from utils.coding import pack_k, unpack_obj, pack_obj, unpack_pub_k
from Domain import PUBLIC_KEY, PRIVATE_KEY, get_json_dict

app = Flask(__name__)
db = DB()
message_queue = MessageQueue()

print("PUBLIC KEY", PUBLIC_KEY.__bytes__())


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


@app.route("/message", methods=['POST'])
def message():
    message = get_json_dict(request)  # расшифрованное своим приватным ключом
    print("MES:", message)
    if message.get(Field.is_junk):
        return "OK", 200
    if message[Field.cypher_count] == 1:
        if message.get(Field.type) == "broadcast":
            db.mail_repo.add_message(recv_pub_k=message[Field.to_pub_k], message=json.dumps(message),
                                     timestamp=message[Field.timestamp])
            print("saved", json.dumps(message))
        else:
            send_broadcast(message)
        return "OK", 200
    send_to_next_node(message)
    return "OK", 200


def send_to_next_node(message):
    message_queue.append_message(MessageTask(url=message[Field.to], data=message[Field.body]))


def send_broadcast(message):
    mixers_pub_keys = get_pub_keys()
    message[Field.type] = "broadcast"
    for server in get_all_servers():
        encrypted = pack_obj(message, mixers_pub_keys[server])  # Зашифровали для получателя
        message_queue.append_message(MessageTask(url=server + "/message", data=encrypted))
    print("sent broadcast", message)


@app.route("/messages", methods=['GET'])
def get_all_messages():
    message = get_json_dict(request)
    print("GETTING UPDATES")
    print(message)
    pub_k = message[Field.sender_public_key]
    return pack_obj({"messages": 1}, pub_k=unpack_pub_k(pub_k))


# def get_updates_for_user(pub_k: str, last_message_time: str, existing_messages_hash):
#     all_messages = db.mail_repo.get_messages_by_recv_pub_k(pub_k)
#     # TODO найти последнее и хэщ префикса, если они совпадают с присланными, то отправить только новые.
#     last_message = all_messages.order_by(.timestamp.desc()).first()
#     return res


@app.route("/user", methods=['POST'])
def register_new_user():
    message_obj = get_json_dict(request)
    pub_k = message_obj[Field.sender_public_key]
    nickname = message_obj[Field.sender_nickname]
    success = db.user_repo.add_user(pub_k, nickname)
    if success:
        for server in get_all_servers():
            message_queue.append_message(MessageTask(url=server + "/user", data=message_obj))
    return "OK", 200


if __name__ == '__main__':
    thread = Thread(target=message_queue.send_mixed, daemon=True)
    thread.start()
    parser = argparse.ArgumentParser()
    parser.add_argument("--xport", dest="xport", default=5000, type=int)
    args = parser.parse_args()
    db.connect(args.xport)
    app.run(port=args.xport, debug=True)

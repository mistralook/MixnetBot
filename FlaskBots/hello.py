import json

import requests
from flask import Flask
from flask import request

from Criptography.cypher import PUBLIC_KEY
from Protocol.field_type import Field
from utils.coding import bytes_to_b64

app = Flask(__name__)


@app.route("/hello", methods=['GET', 'POST'])
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/", methods=['GET', 'POST'])
def mes():
    message = request.get_json(force=True)
    print(message)
    return "ALRIGHT"


# bytes_to_b64(PUBLIC_KEY.encode())
@app.route("/public-key", methods=['POST'])
def get_public_key():
    body = request.get_json()
    response = {"public_key": "some_PK",
                "encoding": "base64"}
    return response


@app.route("/message", methods=['POST'])
def message():
    message = request.get_json(force=True)
    print(message)
    encrypted = message[Field.body]
    decrypted = json.dumps(encrypted)  # пока так потому что дешифратор вернет строчку, а не словарь
    inner = json.loads(decrypted)  # cast str to obj
    if inner[Field.cypher_count] == 1:
        pass  # отправить широковещательно
    # print(inner)
    if inner[Field.cypher_count] > 1:
        send_to_next_node(inner)
    response = {"public_key": bytes_to_b64(PUBLIC_KEY.encode()),
                "encoding": "base64"}
    return "OK", 200


def send_to_next_node(message):
    response = requests.post(url=message[Field.to], json=message[Field.body])
    print(f"Redirected. {response.text}")

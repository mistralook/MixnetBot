import requests
from flask import Flask, request

from Criptography.cypher import PUBLIC_KEY
from Protocol.field_type import MessageType, Field
from utils.coding import bytes_to_b64

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/public-key", methods=['POST'])
def get_public_key():
    body = request.get_json(force=True, silent=False, cache=True)
    sender_pub_k = body[Field.sender_public_key]
    # pub_key_by_sender_id[body[Field.id]] = sender_pub_k
    response = {"public_key": str(bytes_to_b64(PUBLIC_KEY.encode())),
                "encoding": "base64"}
    return response


@app.route("/message", methods=['POST'])
def post_message():
    body = request.get_json(force=True, silent=False, cache=True)
    # Расшифровровать body. Body станет json'ом с 2 полями: to, body
    next_node_ip = body[Field.to]
    response = requests.post(next_node_ip, json=body[Field.body]).content
    print(response)
    return "", 200

import json
import sys

import requests
from nacl.public import PrivateKey, Box
import os.path

sys.path.append('../')
from Prt.field_type import Field
from multiple_encryption import multiple_encrypt
from FlaskBots.Network import get_all_servers


def generate_and_save_keys():
    private = PrivateKey.generate()
    keys = {"private_key": str(private.encode()),
            "public_key": str(private.public_key.encode())}
    name = "keys.json"
    if os.path.isfile(name):
        raise FileExistsError
    with open(name, 'w') as file:
        file.write(json.dumps(keys))


def build_route(recv_pub_k):
    return get_all_servers() + [recv_pub_k]


def send(recv_pub_k, message: str):
    route = build_route(recv_pub_k)
    onion_encrypted = multiple_encrypt(message, route)
    first_node = onion_encrypted[Field.to]
    dumped = json.dumps(onion_encrypted)
    requests.post(url=first_node, json=dumped)
    print(dumped)
    print("sent")

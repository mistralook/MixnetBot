import json

from nacl.public import PrivateKey, Box
import os.path

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
    print(onion_encrypted)

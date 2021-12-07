import json
import sys

import requests
from nacl.public import SealedBox

from DesktopClient.Keys import get_keys
from FlaskBots.Network import get_all_servers
from utils.coding import base64_str_to_public_key, bytes_to_b64

sys.path.append('../')
from Protocol.FieldType import Field


def get_pub_keys():
    pub_key_by_mixer_addr = {}  # key - addr, value - PubKey(from pyNacl)
    for mixer in get_all_servers():
        response = requests.get(f"{mixer}/public-key")
        pub_key = base64_str_to_public_key(response.json()['public_key'])
        pub_key_by_mixer_addr[mixer] = pub_key
    return pub_key_by_mixer_addr


def multiple_encrypt(message_from_user: str, route: list):
    node_pub_keys = get_pub_keys()
    node_pub_keys[route[-1]] = route[-1]
    # route = route[:-1]  # удалили конечного получателя
    rev = list(reversed(route))  # сначала получатель, потом конечный миксер, ..., 1-й миксер
    keys = get_keys()
    cypher_count = 0
    obj = {Field.body: message_from_user,
           Field.to: None,
           Field.sender_pub_k: keys["public_key"],
           Field.cypher_count: cypher_count}
    first_wrapped = True
    for node in rev:
        cypher_count += 1
        box = SealedBox(node_pub_keys[node])
        obj = bytes_to_b64(box.encrypt((str(obj)).encode()))
        obj = {
            # Field.type: MessageType.unencrypted_message,
            Field.body: obj,
            Field.to: f"{node}/message" if not first_wrapped else None,
            Field.to_pub_k: node if first_wrapped else None,
            Field.cypher_count: cypher_count
        }
        first_wrapped = False
    print(obj)
    return obj

import json


from nacl.public import PrivateKey, PublicKey, Box
import os.path
import sys
sys.path.append('../')
from utils.coding import pack_k, unpack_pub_k, unpack_priv_k

name = "keys.json"


class Keys:
    def __init__(self, sk: PrivateKey, pk: PublicKey):
        self.private_key = sk
        self.public_key = pk


def generate_and_save_keys(nickname, force=False):
    private = PrivateKey.generate()
    # print("GENERATING") TODO Delete
    # print(private)
    # print(private.public_key)
    # print("================")
    keys = {"private_key": pack_k(private),
            "public_key": pack_k(private.public_key),
            "nickname": nickname}
    if not force and os.path.isfile(name):
        raise FileExistsError
    with open(name, 'w') as file:
        file.write(json.dumps(keys))


def get_keys():
    if not os.path.isfile(name):
        raise FileNotFoundError
    with open(name, 'r') as file:
        content = file.read()
        return json.loads(content)


def get_keys_f():
    keys = get_keys()
    return Keys(sk=unpack_priv_k(keys["private_key"]),
                pk=unpack_pub_k(keys["public_key"]))

# TODO delete
# generate_and_save_keys("Lol", force=True)
# keys = get_keys_f()
#
# print(keys.private_key)
# print(keys.public_key)

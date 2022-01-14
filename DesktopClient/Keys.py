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








def get_keys_f():
    keys = get_keys()
    return Keys(sk=unpack_priv_k(keys["private_key"]),
                pk=unpack_pub_k(keys["public_key"]))

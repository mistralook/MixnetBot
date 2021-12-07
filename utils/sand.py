import base64
import json
import pickle

import requests
from nacl.public import PrivateKey, PublicKey, SealedBox

from utils.coding import bytes_to_b64, base64_str_to_public_key

#
# def pack_pub_k(key: PublicKey):
#     s = base64.b64encode(key.__bytes__())
#     s = str(s)
#     return s
#
#
# def unpack_pub_k(s: str):
#     bytes_s = base64.b64decode(s[2:-1])
#     return PrivateKey(bytes_s)
#
#
PRIVATE_KEY = PrivateKey.generate()
PUBLIC_KEY = PRIVATE_KEY.public_key





d = {"1": "ab"}
# bad_bytes = pack_obj(d, PUBLIC_KEY)
# print("BAD", bad_bytes)
# # bad_bytes.decode()
# e = base64.b64encode(bad_bytes)
# transporting = str(e)
# print(e)
# restored_bad = base64.b64decode(transporting[2:-1])
# print(restored_bad == bad_bytes)
# print(type(e))
packed = pack_obj(d, PUBLIC_KEY)
print(packed)
print(unpack_obj(packed, PRIVATE_KEY))

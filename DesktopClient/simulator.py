import requests
import json
from nacl.public import PrivateKey
import time

from DesktopClient.multiple_encryption import get_pub_keys
from Domain import send
from FlaskBots.MixServer import get_json_dict
from FlaskBots.Network import get_all_servers
from Protocol.FieldType import Field
from utils.coding import pack_k, pack_obj, unpack_obj

private_key = PrivateKey.generate()
public_key = private_key.public_key

send(public_key, "Oh, hi Mark")

time.sleep(3)

server = get_all_servers()[0]
server_pub_k = get_pub_keys()[server]
message = {"sender_public_key": pack_k(public_key)}
response = requests.get(url=f"{server}/messages", data=pack_obj(message, server_pub_k))
print(response)
d = unpack_obj(data=response.text, sk=private_key)
print(d)
for m in d["messages"]:
    encrypted = json.loads(m)
    unp = unpack_obj(encrypted[Field.body], private_key)
    print(unp)

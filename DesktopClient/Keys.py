import json

from nacl.public import PrivateKey, Box
import os.path

name = "keys.json"


def generate_and_save_keys(nickname):
    private = PrivateKey.generate()
    keys = {"private_key": str(private.encode()),
            "public_key": str(private.public_key.encode()),
            "nickname": nickname}
    if os.path.isfile(name):
        raise FileExistsError
    with open(name, 'w') as file:
        file.write(json.dumps(keys))


def get_keys():
    if not os.path.isfile(name):
        raise FileNotFoundError
    with open(name, 'r') as file:
        content = file.read()
        return json.loads(content)

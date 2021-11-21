import json

from nacl.public import PrivateKey, Box
import os.path


def generate_and_save_keys():
    private = PrivateKey.generate()
    keys = {"private_key": str(private.encode()),
            "public_key": str(private.public_key.encode())}
    name = "keys.json"
    if os.path.isfile(name):
        raise FileExistsError
    with open(name, 'w') as file:
        file.write(json.dumps(keys))

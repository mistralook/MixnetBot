import json
import os
from collections import namedtuple

from nacl.public import PrivateKey, PublicKey

from utils.coding import pack_k, unpack_pub_k, unpack_priv_k

Keys = namedtuple('Keys', ['private', 'public'])


class KeyManager:
    def __init__(self):
        self.filename = "keys.json"

    def try_generate_and_save_keys(self, nickname) -> bool:
        """Returns bool [are keys generated]"""
        try:
            self.generate_and_save_keys(nickname, force=False)
            return True
        except FileExistsError:
            return False

    def generate_and_save_keys(self, nickname, force=False):
        private = PrivateKey.generate()
        keys = {"private_key": pack_k(private),
                "public_key": pack_k(private.public_key),
                "nickname": nickname}
        if self.keys_are_generated and not force:
            raise FileExistsError
        with open(self.filename, 'w') as file:
            file.write(json.dumps(keys))

    @property
    def keys_are_generated(self):
        return os.path.isfile(self.filename)

    @property
    def pk_packed(self) -> PublicKey:
        return self.get_keys().public

    @property
    def sk_packed(self):
        return self.get_keys().private

    @property
    def pk(self) -> PublicKey:
        return unpack_pub_k(self.get_keys().public)

    @property
    def sk(self) -> PrivateKey:
        return unpack_priv_k(self.get_keys().private)

    def _get_keys_from_file(self):
        if not os.path.isfile(self.filename):
            raise FileNotFoundError
        with open(self.filename, 'r') as file:
            content = file.read()
            return json.loads(content)

    def get_keys(self):
        keys_dict = self._get_keys_from_file()
        return Keys(public=keys_dict["public_key"],
                    private=keys_dict["private_key"])

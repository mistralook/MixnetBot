import nacl.utils
from nacl.public import PrivateKey, Box


PRIVATE_KEY = PrivateKey.generate()
PUBLIC_KEY = PRIVATE_KEY.public_key


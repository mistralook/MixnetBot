import nacl.utils
from nacl.public import PrivateKey, Box


PRIVATE_KEY = PrivateKey.generate()
PUBLIC_KEY = PRIVATE_KEY.public_key

if __name__ == "__main__":
    print(PUBLIC_KEY._public_key)
    # print(PUBLIC_KEY)
import base64
import json
import hashlib
from nacl import encoding

from nacl.public import PublicKey, SealedBox, PrivateKey


def bytes_to_b64(cypher_key: bytes):
    return base64.b64encode(cypher_key)


def b64to_bytes(b64string: str):  # принимает b'some_bytes'
    return base64.b64decode(b64string[2:-1])


def base64_str_to_public_key(s: str):  # принимает b'some_bytes'
    bytes_s = base64.b64decode(s[2:-1])
    return PublicKey(bytes_s)  # , encoder=encoding.Base64Encoder


def base64_str_to_private_key(s: str):
    bytes_s = base64.b64decode(s)
    return PrivateKey(bytes_s)  # , encoder=encoding.Base64Encoder


def pack_k(key: PublicKey) -> str:
    s = base64.b64encode(key.__bytes__())
    s = str(s)
    return s


def unpack_pub_k(s: str) -> PublicKey:
    bytes_s = base64.b64decode(s[2:-1])
    return PublicKey(bytes_s)


def unpack_priv_k(s: str) -> PrivateKey:
    bytes_s = base64.b64decode(s[2:-1])
    return PrivateKey(bytes_s)


def pack_obj(obj, pub_k: PublicKey) -> str:
    box = SealedBox(pub_k)
    data = json.dumps(obj).encode()
    b = box.encrypt(data)
    return str(base64.b64encode(b))


def unpack_obj(data: str, sk: PrivateKey) -> dict:
    b = base64.b64decode(data[2:-1])
    box = SealedBox(sk)
    r_str = box.decrypt(b).decode()
    return json.loads(r_str)


def get_hash_of_uids(uids):
    s = "".join(map(str, uids))
    hash_object = hashlib.sha256(s.encode())
    return hash_object.hexdigest()


if __name__ == '__main__':
    PRIVATE_KEY = PrivateKey.generate()
    PUBLIC_KEY = PRIVATE_KEY.public_key
    d = {"1": "ab"}
    print(pack_obj(d, PUBLIC_KEY))
    # print(unpack_obj(pack_obj(d, PUBLIC_KEY), PRIVATE_KEY))

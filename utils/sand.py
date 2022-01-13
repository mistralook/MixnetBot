import base64
import json

from nacl.public import SealedBox, PrivateKey, PublicKey, Box


def pack_str(s: str, priv_k, pub_k: PublicKey) -> str:
    box = Box(priv_k, pub_k)
    data = json.dumps(s).encode()
    b = box.encrypt(data)
    return str(base64.b64encode(b))


def unpack_str(data: str, sk: PrivateKey, pk) -> str:
    b = base64.b64decode(data[2:-1])
    box = Box(sk, pk)
    r_str = box.decrypt(b).decode()
    return json.loads(r_str)


d = "Hi mark"
a_sk = PrivateKey.generate()
a_pk = a_sk.public_key

b_sk = PrivateKey.generate()
b_pk = b_sk.public_key

packed = pack_str(d, a_sk, b_pk)
print(packed)
print(type(packed))
unpacked = unpack_str(packed, b_sk, a_pk)

print(unpacked)
print(type(unpacked))

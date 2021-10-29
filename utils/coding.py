import base64
from nacl import encoding

from nacl.public import PublicKey


def bytes_to_b64(cypher_key: bytes):
    return base64.b64encode(cypher_key)


def b64to_bytes(b64string: str):
    return base64.b64decode(b64string)


def base64_str_to_public_key(s: str):
    bytes_s = base64.b64decode(s)
    return PublicKey(bytes_s)  # , encoder=encoding.Base64Encoder


def base64_str_to_private_key(s: str):
    bytes_s = base64.b64decode(s)
    return PrivateKey(bytes_s)  # , encoder=encoding.Base64Encoder

# s = b"abaoba"
# print(b64to_bytes(bytes_to_b64(s)))

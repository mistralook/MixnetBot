import base64
from nacl import encoding

from nacl.public import PublicKey


def cypher_key_to_base64(cypher_key: bytes):
    b64encoded = base64.b64encode(cypher_key)
    return str(b64encoded)[2:-1]


def base64_str_to_public_key(s: str):
    bytes_s = base64.b64decode(s)
    return PublicKey(bytes_s)  # , encoder=encoding.Base64Encoder

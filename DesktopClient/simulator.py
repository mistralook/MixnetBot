from nacl.public import PrivateKey

from Domain import send

public_key = PrivateKey.generate().public_key

send(public_key, "Oh, hi Mark")

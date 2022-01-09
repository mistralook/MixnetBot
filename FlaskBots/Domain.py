from nacl.public import PrivateKey, SealedBox

from coding import unpack_obj

PRIVATE_KEY = PrivateKey.generate()
PUBLIC_KEY = PRIVATE_KEY.public_key


def get_json_dict(request) -> dict:
    data = request.get_data()
    return unpack_obj(data=data, sk=PRIVATE_KEY)

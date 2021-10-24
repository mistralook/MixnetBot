from nacl.public import Box

from utils.coding import base64_str_to_public_key

PRIVATE_KEY = b'\xceg\xe8\xd4\xc9\x15R\xcaN\x990\xb7\xc4\xef\xd5.\x08B\xd1\xe4\xe3\xa9W\xf8"@@~\x109S+'
bot_pub_key = base64_str_to_public_key("qgjjZrwuDd4otX8O+/awlwjYzeekCxQIICrfVw2KYgE=")

our_box = Box(PRIVATE_KEY, bot_pub_key)
encrypted = our_box.encrypt(b"Hello form user")
print(encrypted)

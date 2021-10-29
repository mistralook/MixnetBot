from nacl.public import Box, PrivateKey

from utils.coding import base64_str_to_public_key

PRIVATE_KEY_USER = PrivateKey(
    b'#"\xac\x9e\xaf\x0f*W\x17\xe0\xd0\x86\x06\xbcH\x03\xcb\xb5\x14\x8e\xe6W\xd2+\xae\xd6\x19q\xa9VY\xb9')

PRIVATE_KEY_BOT = PrivateKey(b'\xb3J\t!Va\x88\xd4\xf9J!L\x16mr\xe7\xc5XlR\xba\xe8\x06]\xd6\xb8\xe0\xac\xb3\x08\x03\x9d')
bot_pub_key = base64_str_to_public_key("bTM84Vz7zcX6ngD43wCphfGt8cPQYNbtWXpQuvrVuhI=")

our_box = Box(PRIVATE_KEY, bot_pub_key)
encrypted = our_box.encrypt(b"Hello form user")
print(encrypted)

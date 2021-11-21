import config

from Bots.MixerBot import MixerBot
from Criptography.cypher import *
from utils.coding import bytes_to_b64
from config import *

if __name__ == '__main__':
    private_k = PrivateKey.generate()
    public_k = private_k.public_key
    print(f"user pub k : {public_k}")

    print(f"user priv k : {private_k}")

    print(f"user pub k b64 : {bytes_to_b64(public_k.encode())}")
    print(f"user priv k b64 : {bytes_to_b64(private_k.encode())}")
    print(f" BOT pub_k 64: {bytes_to_b64(PUBLIC_KEY.encode())}")
    print(f" BOT priv_k 64: {bytes_to_b64(PRIVATE_KEY.encode())}")
    print(f" BOT priv_k: {PRIVATE_KEY.encode()}")
    bot = MixerBot(config.token1)
    bot.run()

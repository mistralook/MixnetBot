import base64

from telegram import Update
from telegram.ext import CallbackContext, Updater, Filters, MessageHandler
import config
import json
from Protocol.field_type import MessageType, Field
from Criptography.cypher import *
from utils.coding import bytes_to_b64, base64_str_to_public_key, b64to_bytes

pub_key_by_sender_id = {}  # значения в b64


def ping_handler(update, context):
    update.message.reply_text(text="pong")


def get_pub_key_handler(update, context, message: json):
    sender_pub_key = message[Field.sender_public_key]
    pub_key_by_sender_id[update.message.from_user.id] = sender_pub_key
    response = {"public_key": bytes_to_b64(PUBLIC_KEY.encode()),
                "encoding": "base64"}
    update.message.reply_text(text=json.dumps(response))


def decipher_handler(update, context, message: json):
    sender_pub_key_b64 = pub_key_by_sender_id[update.message.from_user.id]
    sender_pub_key = base64_str_to_public_key(sender_pub_key_b64)
    print(f"sender_pub_k29: {sender_pub_key}")
    our_box = Box(PRIVATE_KEY, sender_pub_key)
    encrypted = message[Field.body]
    decrypted = our_box.decrypt(encrypted)
    update.message.reply_text(text=decrypted)


def router(update, context):
    try:
        print(update.message.text)
        message = json.loads(update.message.text)
    except Exception as e:
        update.message.reply_text(text="Invalid message")
        print(e)
        return
    if message[Field.type] == MessageType.ping:
        ping_handler(update, context)
        return
    if message[Field.type] == MessageType.get_public_key:
        get_pub_key_handler(update, context, message)
        return
    if message[Field.type] == MessageType.message:
        decipher_handler(update, context, message)
        return
    update.message.reply_text(text="I'm a teapot")
    print("Answered")


def main():
    print('Bot started')
    updater = Updater(
        token=config.token,
        use_context=True
    )
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.text,
                                                  callback=router))

    updater.start_polling()
    updater.idle()


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
    main()

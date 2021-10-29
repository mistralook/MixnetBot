from telegram import Update
from telegram.ext import CallbackContext, Updater, Filters, MessageHandler
import config
import json
from Protocol.field_type import MessageType, Field
from Criptography.cypher import *
from utils.coding import bytes_to_b64, base64_str_to_public_key, b64to_bytes


class MixerBot:
    def __init__(self, token):
        self.pub_key_by_sender_id = {}  # значения в b64
        self.token = token

    def ping_handler(self, update, context):
        update.message.reply_text(text="pong")

    def get_pub_key_handler(self, update, context, message: json):
        sender_pub_key = message[Field.sender_public_key]
        self.pub_key_by_sender_id[update.message.from_user.id] = sender_pub_key
        response = {"public_key": bytes_to_b64(PUBLIC_KEY.encode()),
                    "encoding": "base64"}
        update.message.reply_text(text=json.dumps(response))

    def decipher_handler(self, update, context, message: json):
        sender_pub_key_b64 = self.pub_key_by_sender_id[update.message.from_user.id]
        sender_pub_key = base64_str_to_public_key(sender_pub_key_b64)
        print(f"sender_pub_k29: {sender_pub_key}")
        our_box = Box(PRIVATE_KEY, sender_pub_key)
        encrypted = message[Field.body]
        decrypted = b64to_bytes(our_box.decrypt(encrypted))
        update.message.reply_text(text=decrypted)

    def router(self, update, context):
        try:
            print(update.message.text)
            message = json.loads(update.message.text)
        except Exception as e:
            update.message.reply_text(text="Invalid message")
            print(e)
            return
        if message[Field.type] == MessageType.ping:
            self.ping_handler(update, context)
            return
        if message[Field.type] == MessageType.get_public_key:
            self.get_pub_key_handler(update, context, message)
            return
        if message[Field.type] == MessageType.message:
            self.decipher_handler(update, context, message)
            return
        update.message.reply_text(text="I'm a teapot")
        print("Answered")

    def start(self):
        print('Bot started')
        updater = Updater(
            token=self.token,
            use_context=True
        )
        updater.dispatcher.add_handler(MessageHandler(filters=Filters.text,
                                                      callback=self.router))

        updater.start_polling()
        updater.idle()

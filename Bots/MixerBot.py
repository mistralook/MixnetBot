import requests
from telegram import Update
import telegram
from telegram.ext import CallbackContext, Updater, Filters, MessageHandler, CommandHandler
import config
import json
from Protocol.field_type import MessageType, Field
from Criptography.cypher import *
from utils.coding import bytes_to_b64, base64_str_to_public_key, b64to_bytes


class MixerBot:
    def __init__(self, token):
        self.pub_key_by_sender_id = {}  # значения в b64
        self.token = token

    def start(self, update: Update, context: CallbackContext) -> None:
        """Sends explanation on how to use the bot."""
        update.message.reply_text('Hi!')

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

    def unencrypted_message_handler(self, update, context, message):
        print("UNENCRYPTED")
        print(message)
        body = message[Field.body]
        to = body[Field.to]
        sender_chat_id = update.effective_chat.id
        sent_mes = context.bot.send_message(chat_id=to, text="Hello from first",
                                            allow_sending_without_reply=True)
        print("sent")
        print(sent_mes)

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
        if message[Field.type] == MessageType.unencrypted_message:
            self.unencrypted_message_handler(update, context, message)
            return
        update.message.reply_text(text="I'm a teapot")
        print("Answered")

    def run(self):
        print('Bot started')
        updater = Updater(
            token=self.token,
            use_context=True
        )
        # print(updater.bot)
        updater.dispatcher.add_handler(CommandHandler("start", self.start))
        updater.dispatcher.add_handler(CommandHandler("ping", self.ping_handler))
        updater.dispatcher.add_handler(MessageHandler(filters=Filters.text,
                                                      callback=self.router))

        updater.start_polling()
        updater.idle()


requests.post()
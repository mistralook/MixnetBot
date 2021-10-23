import base64

from telegram import Update
from telegram.ext import CallbackContext, Updater, Filters, MessageHandler
import config
import json
from Protocol.field_type import FieldType, Field
from Criptography.cypher import *


def ping_handler(update, context):
    update.message.reply_text(text="pong")


def get_pub_key_handler(update, context):
    b64encoded = base64.b64encode(PUBLIC_KEY.encode())
    response = {"public_key": str(b64encoded)[2:-1],
                "encoding": "base64"}
    update.message.reply_text(text=json.dumps(response))


def router(update, context):
    try:
        print(update.message.text)
        message = json.loads(update.message.text)
    except Exception as e:
        update.message.reply_text(text="Invalid message")
        print(e)
        return
    if message[Field.type] == FieldType.ping:
        ping_handler(update, context)
        return
    if message[Field.type] == FieldType.get_public_key:
        get_pub_key_handler(update, context)
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
    main()

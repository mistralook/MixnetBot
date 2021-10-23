from telegram import Update
from telegram.ext import CallbackContext, Updater, Filters, MessageHandler
import config


def handler(update, context):
    print(f"Received: {update.message.text}")
    update.message.reply_text(text="I'm a teapot")
    print("Answered")


def main():
    print('Bot started')
    updater = Updater(
        token=config.token,
        use_context=True
    )
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.text,
                                                  callback=handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

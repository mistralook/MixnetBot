from telethon import TelegramClient

# Вставляем api_id и api_hash
from DesktopClient.config import API_ID, API_HASH

client = TelegramClient('Session in mixer client', API_ID, API_HASH)
client.start()

# for dialog in client.iter_dialogs():
#     print(dialog.title)


async def main():
    # Getting information about yourself
    me = await client.get_me()
    await client.send_message('+7 904 982 6823', "Привет, мам")


with client:
    client.loop.run_until_complete(main())

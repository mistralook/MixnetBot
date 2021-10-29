from telethon import TelegramClient

# Вставляем api_id и api_hash
from DesktopClient.config import API_ID, API_HASH
from DesktopClient.multiple_encryption import multiple_encrypt
from DesktopClient.user_input import get_user_input

client = TelegramClient('Session in mixer client', API_ID, API_HASH)
client.start()


# for dialog in client.iter_dialogs():
#     print(dialog.title)


async def main():
    me = await client.get_me()
    route = ['@OnionMixer1Bot', '@OnionMixer2Bot', me.username]  # должно приходить обратно к отправителю
    onion_wrapped = multiple_encrypt(message_from_user=get_user_input(), route=route)
    await client.send_message(route[0], onion_wrapped)


with client:
    client.loop.run_until_complete(main())

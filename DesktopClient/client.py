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
    id_by_name = {'@OnionMixer1Bot': "2060785008",
                  '@OnionMixer2Bot': "2027385873",
                  me.username: "81361925"}
    print(me)
    route = [id_by_name['@OnionMixer1Bot'],
             id_by_name['@OnionMixer2Bot'],
             id_by_name[me.username]]  # должно приходить обратно к отправителю
    onion_wrapped = multiple_encrypt(message_from_user=get_user_input(), route=route)
    await client.send_message('@OnionMixer1Bot', onion_wrapped)


with client:
    client.loop.run_until_complete(main())

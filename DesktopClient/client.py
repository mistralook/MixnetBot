from telethon import TelegramClient

# Вставляем api_id и api_hash
from DesktopClient.config import API_ID, API_HASH

client = TelegramClient('Session in mixer client', API_ID, API_HASH)
client.start()

# await client.send_message('@Batislavich', """Ярославик, здорово,
#  это сообщение из нашего питоновского телеграм-клиента""")


for dialog in client.iter_dialogs():
    print(dialog.title)
from DesktopClient.multiple_encryption import multiple_encrypt
from DesktopClient.user_input import get_user_input

id_by_name = {'@OnionMixer1Bot': "2060785008",
              '@OnionMixer2Bot': "2027385873",
              "me": "81361925"}
route = [id_by_name['@OnionMixer1Bot'],
         id_by_name['@OnionMixer2Bot']
         ]
onion_wrapped = multiple_encrypt(message_from_user=get_user_input(), route=route)
# await client.send_message('@OnionMixer1Bot', onion_wrapped)
print(onion_wrapped)

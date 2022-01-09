from DesktopClient.Keys import get_keys_f
from Domain import send

# # private_key = PrivateKey.generate()
# # public_key = private_key.public_key
#
# private_key = PrivateKey(
#     b'L\xcf\\\xb5\xb9RSly\x81\xae\xf7\x9b\xdc\xcao\xca\xb1],\xd0$\x03\xbd\xfc\xe6\xd7z\xa4\xdd\xcc\x85')
# public_key = private_key.public_key
# print(private_key)
# print("-------------")
# print(public_key)

recv_keys = get_keys_f()
public_key = recv_keys.public_key
private_key = recv_keys.private_key
send(public_key, "RR!")

# time.sleep(3)
#
# server = get_all_servers()[0]
# server_pub_k = get_pub_keys()[server]
# message = {"sender_public_key": pack_k(public_key)}
# response = requests.get(url=f"{server}/messages", data=pack_obj(message, server_pub_k))
# d = unpack_obj(data=response.text, sk=private_key)
# for m in d["messages"]:
#     encrypted = json.loads(m)
#     unp = unpack_obj(encrypted[Field.body], private_key)
#     sender = unp[Field.sender_pub_k]
#     print(sender)
#     print(unp)

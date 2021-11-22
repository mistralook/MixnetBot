import json
import sys

from DesktopClient.Keys import get_keys

sys.path.append('../')
from Prt.field_type import Field


def multiple_encrypt(message_from_user: str, route: list):
    recv_pub_k = route[-1]
    # route = route[:-1]  # удалили конечного получателя
    rev = list(reversed(route))  # сначала получатель, потом конечный миксер, ..., 1-й миксер
    keys = get_keys()
    obj = {Field.body: message_from_user,
           Field.to: None,
           Field.sender_pub_k: keys["public_key"],
           Field.cypher_count: 0}
    first_wrapped = True
    for node in rev:
        obj = {
            # Field.type: MessageType.unencrypted_message,
            Field.body: obj,
            Field.to: f"{node}/message" if not first_wrapped else None,
            Field.to_pub_k: node if first_wrapped else None,
            Field.cypher_count: obj[Field.cypher_count] + 1
        }
        first_wrapped = False
    return obj

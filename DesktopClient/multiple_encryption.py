import json
import sys

sys.path.append('../')
from Prt.field_type import Field


def multiple_encrypt(message_from_user: str, route: list):
    rev = list(reversed(route))  # сначала получатель, потом конечный миксер, ..., 1-й миксер
    obj = message_from_user
    for node in rev:
        obj = {
            # Field.type: MessageType.unencrypted_message,
            Field.body: obj,
            Field.to: node
        }
    res = json.dumps(obj, ensure_ascii=False)
    # print(res)
    return res

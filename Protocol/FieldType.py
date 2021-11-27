class MessageType:
    message = "message"
    ping = "ping"
    get_public_key = "get_public_key"
    unencrypted_message = "unencrypted_message"


class Field:
    type = "type"
    body = "body"
    to = "to"
    to_pub_k = "to_pub_k"
    sender_pub_k = "sender_pub_k"
    id = "id"
    sender_public_key = "sender_public_key"
    cypher_count = "cypher_count"  # показывает во сколько шифров обернуто body, находящееся на этой же глубине

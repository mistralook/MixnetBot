class MessageType:
    message = "message"
    ping = "ping"
    get_public_key = "get_public_key"
    unencrypted_message = "unencrypted_message"


class Field:
    type = "type"
    body = "body"
    to = "to"  # кому нужно отправить body, находящееся на этой же глубине. Только он сможет его открыть
    to_pub_k = "to_pub_k"
    sender_pub_k = "sender_pub_k"
    sender_nickname = "sender_nickname"
    id = "id"
    is_junk = "is_junk"
    sender_public_key = "sender_public_key"
    cypher_count = "cypher_count"  # показывает во сколько шифров обернуто body, находящееся на этой же глубине

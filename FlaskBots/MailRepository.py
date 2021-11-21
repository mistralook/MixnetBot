from collections import defaultdict


class MailRepository:
    def __init__(self):
        self.storage = defaultdict(set)

    def add_message(self, recv_pub_k, message):
        self.storage[recv_pub_k].add(message)

    def get_messages_by_recv_pub_k(self, recv_pub_k):
        return list(self.storage[recv_pub_k])

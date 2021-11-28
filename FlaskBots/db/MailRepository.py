from collections import defaultdict

from db.DBModels import Message


class MailRepository:
    def __init__(self):
        self.storage = defaultdict(set)

    def add_message(self, recv_pub_k, message):
        created = Message(pub_k=recv_pub_k, text=message)
        created.save()

    def get_messages_by_recv_pub_k(self, recv_pub_k):
        query = Message.select().where(Message.pub_k == recv_pub_k)
        messages_selected = query.namedtuples().execute()
        return [record.text for record in messages_selected]

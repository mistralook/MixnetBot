from collections import defaultdict
from peewee import *

conn = SqliteDatabase('mails.sqlite')
conn.connect()


class BaseModel(Model):
    class Meta:
        database = conn


class Message(BaseModel):
    message_id = AutoField(column_name='MessageId')
    pub_k = TextField(column_name='Pub_K', null=False)
    text = TextField(column_name='Message_text', null=False)

    class Meta:
        table_name = 'Message'


conn.create_tables([Message])


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

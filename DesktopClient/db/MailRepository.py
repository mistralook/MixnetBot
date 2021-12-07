from collections import defaultdict
from peewee import *

conn = SqliteDatabase('db/mails.sqlite')
conn.connect()


class BaseModel(Model):
    class Meta:
        database = conn


class Message(BaseModel):
    message_id = AutoField(column_name='MessageId')
    sender_pub_k = TextField(column_name='Sender_pub_K', null=False)
    text = TextField(column_name='Message_text', null=False)

    class Meta:
        table_name = 'Message'


conn.create_tables([Message])


class MailRepository:

    def add_message(self, sender_pub_k, message):
        created = Message(sender_pub_k=sender_pub_k, text=message)
        created.save()

    def get_messages_by_sender_pub_k(self, sender_pub_k):
        query = Message.select().where(Message.sender_pub_k == sender_pub_k)
        messages_selected = query.namedtuples().execute()
        return messages_selected
        # return [record.text for record in messages_selected]

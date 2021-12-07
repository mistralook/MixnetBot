import peewee
from peewee import *

conn = SqliteDatabase('db/mails.sqlite')
conn.connect()


class BaseModel(Model):
    class Meta:
        database = conn


class Message(BaseModel):
    message_id = CharField(column_name='MessageId', primary_key=True)
    sender_pub_k = TextField(column_name='Sender_pub_K', null=False)
    text = TextField(column_name='Message_text', null=False)

    class Meta:
        table_name = 'Message'


conn.create_tables([Message])


class UserMailRepository:
    def add_message(self, sender_pub_k, message, id):
        created = Message(message_id=id, sender_pub_k=sender_pub_k, text=message)
        try:
            created.save()
            return True
        except peewee.IntegrityError:
            return False

    def get_messages_by_sender_pub_k(self, sender_pub_k):
        query = Message.select().where(Message.sender_pub_k == sender_pub_k)
        messages_selected = query.namedtuples().execute()
        return messages_selected
        # return [record.text for record in messages_selected]

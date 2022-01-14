import datetime

from dateutil import parser
from peewee import *
import sys

from utils.coding import get_hash_of_uids

sys.path.append('../')

conn = SqliteDatabase('db/mails.sqlite')
conn.connect()


class BaseModel(Model):
    class Meta:
        database = conn


class Message(BaseModel):
    message_id = AutoField(column_name='MessageId')
    sender_pub_k = TextField(column_name='Sender_pub_K', null=False)
    text = TextField(column_name='Message_text', null=False)
    timestamp = DateTimeField(column_name="sending_time", null=False)
    uid = TextField(column_name="uid", null=False)

    class Meta:
        table_name = 'Message'


class User(BaseModel):
    pub_k = TextField(column_name='pub_k', null=False)
    name = TextField(column_name='name', null=False)

    class Meta:
        table_name = 'User'


conn.create_tables([Message, User])


class MailRepository:
    def add_message(self, sender_pub_k, message, timestamp: str, uid: int):
        created = Message(sender_pub_k=sender_pub_k, text=message,
                          timestamp=parser.parse(timestamp),
                          uid=str(uid))
        created.save()

    def get_messages_by_sender_pub_k(self, sender_pub_k):
        query = Message.select().where(Message.sender_pub_k == sender_pub_k)
        messages_selected = query.namedtuples().execute()
        return messages_selected

    def get_last_message_time(self):
        last_message = Message.select().order_by(Message.timestamp.desc()).first()
        if last_message:
            return last_message.timestamp.isoformat()  # returning str
        return None

    def get_all_messages_hash(self):
        uids = [m.uid for m in Message.select()]
        return get_hash_of_uids(uids)

    def get_all_senders(self):
        return list(set(m.sender_pub_k for m in Message.select()))

    def add_user(self, name, pub_k):
        User(name=name, pub_k=pub_k).save()

    def get_user_pub_k(self, name):
        res = User.get(User.name == name)
        if not res:
            return None
        return res

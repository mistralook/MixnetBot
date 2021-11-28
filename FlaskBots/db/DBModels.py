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


class User(BaseModel):
    pub_k = TextField(column_name='Pub_K', null=False, unique=True)
    nickname = TextField(column_name='nickname', null=False)


conn.create_tables([Message, User])

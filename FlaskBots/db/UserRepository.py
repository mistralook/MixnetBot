import peewee

from db.DBModels import User


class UserRepository:
    def add_user(self, pub_k, nickname):
        created = User(pub_k=pub_k, nickname=nickname)
        try:
            created.save()
            return True
        except peewee.IntegrityError:
            return False

    def get_user_by_pub_k(self, pub_k):
        return User.select().where(User.pub_k == pub_k).get()

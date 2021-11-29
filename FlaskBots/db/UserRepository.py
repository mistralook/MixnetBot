import peewee


class UserRepository:
    def __init__(self, user_model):
        self.user_model = user_model

    def add_user(self, pub_k, nickname):
        created = self.user_model(pub_k=pub_k, nickname=nickname)
        try:
            created.save()
            return True
        except peewee.IntegrityError:
            return False

    def get_user_by_pub_k(self, pub_k):
        return self.user_model.select().where(self.user_model.pub_k == pub_k).get()

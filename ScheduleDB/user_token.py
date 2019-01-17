from users import *


class UserToken:
    def __init__(self, user):
        self.user = user

    def get_user(self):
        return self.user

    def is_anon(self):
        return type(self.user) is None

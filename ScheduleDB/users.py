import abc
from abc import ABCMeta

privileges = [
    "ADMIN",
    "USER"
]


class BaseUser(metaclass=ABCMeta):
    def __init__(self, login, raw_password):
        self.login = login
        self.raw_password = raw_password

    def get_login(self):
        return self.login

    def get_raw_password(self):
        return self.raw_password

    @abc.abstractmethod
    def get_privileges(self):
        return


class User(BaseUser):
    def __init__(self, login, raw_password):
        super().__init__(login, raw_password)

    def get_privileges(self):
        return privileges[1]


class Admin(BaseUser):
    def __init__(self, login, raw_password):
        super().__init__(login, raw_password)

    def get_privileges(self):
        return privileges[0]

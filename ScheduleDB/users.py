import abc
from abc import ABCMeta

privileges = {
    "ADMIN": 1,
    "USER": 2
}


class BaseUser(metaclass=ABCMeta):
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def get_login(self):
        return self.login

    def get_password(self):
        return self.password

    @abc.abstractmethod
    def get_privileges(self):
        return


class User(BaseUser):
    def __init__(self, login, password):
        super().__init__(login, password)

    def get_privileges(self):
        return privileges["USER"]


class Admin(BaseUser):
    def __init__(self, login, password):
        super().__init__(login, password)

    def get_privileges(self):
        return privileges["ADMIN"]

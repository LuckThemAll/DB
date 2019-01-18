import hashlib

from user_token import UserToken


def password_verify(raw_pass, hash_pass):
    raw_pass = str.encode(raw_pass)
    hash_raw_pass = hashlib.md5(raw_pass).hexdigest()

    return hash_pass == hash_raw_pass


class AuthenticateService:
    def __init__(self, user_repos):
        self.user_repository = user_repos

    def authenticate_by_bred(self, credentials):
        if credentials:
            cred_list = credentials.split("#")
            login = cred_list[0]
            hash_pass = cred_list[1]
            user = self.user_repository.find_by_login(login)
            if user is None:
                return UserToken(None)

            if hash_pass == user.get_password():
                return UserToken(user)
        return UserToken(None)

    def authenticate_by_log_pass(self, login, raw_pass):
        if login.__len__() > 0 and raw_pass.__len__() > 0:
            user = self.user_repository.find_by_login(login)

            if user is None:
                return UserToken(None)

            if user and password_verify(raw_pass, user.get_password()):
                return UserToken(user)

        return UserToken(None)

    def generate_credentials(self, user):
        db_user = self.user_repository.find_by_login(user.get_login())
        if db_user and user.get_password() == db_user.get_password():
            cred = user.get_login() + "#" + user.get_password()
            return cred
        return None

from db_connect import *
from misc import *

from users import Admin, User, privileges


class UserRepository:
    def __init__(self):
        self.table_name = "USERS"

    def find_by_login(self, login):
        query = "select * from " + self.table_name + " where login = ? ;"
        cur.execute(query, get_list(login))
        result = cur.fetchone()
        if result is not None:
            cred = int(result[3])
            login = result[1]
            password = result[2]
            if cred == privileges["ADMIN"]:
                return Admin(login, password)
            elif cred == privileges["USER"]:
                return User(login, password)
        return None

    def save_user(self, user=None):
        if user:
            query = "insert into " + self.table_name + "(login, pass, cred) values (?,?,?)"
            params = [user.get_login(), user.get_password(), user.get_privileges()]
            print("_____________________________s")
            print(params)
            cur.execute(query, params)
            cur.transaction.commit()




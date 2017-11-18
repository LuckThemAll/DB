import fdb


def db_connect():
    connection = fdb.connect(
        dsn='localhost:C:/Users/Artem/Desktop/DB/TIMETABLE.FDB',
        user='SYSDBA',
        password='masterkey',
        charset='UTF8'
    )
    return connection


con = db_connect()
cur = con.cursor()

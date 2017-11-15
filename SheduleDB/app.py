from flask import Flask
from flask import request
from flask import render_template
from abc import *
import fdb


app = Flask(__name__)


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


def get_tables():
    tables = (
        'AUDIENCES',
        'GROUPS',
        'LESSONS',
        'LESSON_TYPES',
        'SCHED_ITEMS',
        'SUBJECTS',
        'SUBJECT_GROUP',
        'SUBJECT_TEACHER',
        'TEACHERS',
        'WEEKDAYS',
    )
    return tables


class NamedModel(metaclass=ABCMeta):
    def __init__(self, title, pixels, table_name):
        super().__init__()
        self.id = {'col_name': 'ID', 'title': 'Ключ', 'pixels': 20}
        self.name = {'col_name': 'NAME', 'title': title, 'pixels': pixels}
        self.table_name = table_name

    def get_name(self):
        sql = 'select %s from %s' % (self.name['col_name'], self.table_name)
        if cur.execute(sql):
            return [col[0] for col in cur.fetchall()]

    def get_id(self):
        sql = 'select %s from %s' % (self.id['col_name'], self.table_name)
        if cur.execute(sql):
            return [col[0] for col in cur.fetchall()]

    def find_one(self, id):
        sql = 'select NAME from %s s where s.ID=%d' % (self.table_name, id)
        if cur.execute(sql):
            return cur.fetchall()[0][0]

    def get_title(self):
        return self.name['title']


class Audiences(NamedModel):
    def __init__(self):
        super().__init__('Номер аудитории', 50, 'AUDIENCES')


class Groups(NamedModel):
    def __init__(self):
        super().__init__('Группа', 50, 'GROUPS')


class Subjects(NamedModel):
    def __init__(self):
        super().__init__('Предмет', 100, 'SUBJECTS')


class SubjectGroup:
    def __init__(self):
        self.subject_ids = {'column': self.get_subject_id(), 'title': Subjects().get_title()}
        self.group_ids = {'column': self.get_group_id(), 'title': Groups().get_title()}

    @staticmethod
    def get_subject_id():
        sql = 'select SUBJECT_ID from SUBJECT_GROUP'
        if cur.execute(sql):
            return [col for col in cur.fetchall()]

    @staticmethod
    def get_subject(id):
        Subjects().find_one(id)

    @staticmethod
    def get_group_id():
        sql = 'select GROUP_ID from SUBJECT_GROUP'
        if cur.execute(sql):
            return [col for col in cur.fetchall()]

    @staticmethod
    def get_group(id):
        Groups().find_one(id)

    # group_id = ['Ref', Subjects, 'id']


def get_headers(selected_table):
     cur.execute('''select RDB$FIELD_NAME from RDB$RELATION_FIELDS
                    where RDB$RELATION_NAME = \'''' + get_tables()[selected_table] + ' \' ')
     return [item[0] for item in cur.fetchall()]


def get_records(selected_table):
    cur.execute('select * from ' + get_tables()[selected_table])
    return cur.fetchall()


@app.route('/')
def index():
    data = {}
    tables = get_tables()
    data['tables'] = tables

    con = db_connect()
    cur = con.cursor()
    selected_table = request.args.get('tables', '')
    if (selected_table.isdigit() and int(selected_table) >= 0 and int(selected_table) < len(tables)):
        selected_table = int(selected_table)
        data['selected_table'] = selected_table
        data['headers'] = get_headers(selected_table, cur)
        data['records'] = get_records(selected_table, cur)
    return render_template('back_ground.html', **data)


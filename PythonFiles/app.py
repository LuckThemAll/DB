from flask import Flask
from flask import request
from flask import render_template
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


def get_headers(selected_table, cur):
     cur.execute('''select RDB$FIELD_NAME from RDB$RELATION_FIELDS
                    where RDB$RELATION_NAME = \'''' + get_tables()[selected_table] + ' \' ')
     return [item[0] for item in cur.fetchall()]


def get_records(selected_table, cur):
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


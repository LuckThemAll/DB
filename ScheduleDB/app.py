from flask import Flask
from flask import request
from flask import render_template
from models import *

app = Flask(__name__)


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



@app.route('/')
def index():
    data = {}
    tables = get_tables()
    data['tables'] = tables
    selected_table = request.args.get('tables', '')
    if (selected_table.isdigit() and int(selected_table) >= 0 and int(selected_table) < len(tables)):

        mem = Audiences()
        print(mem.columns)
        print(mem.get_titles())
        print('---------------------------')
        mem = SubjectTeacher()
        print(mem.columns)
        print(mem.get_titles())
        print('---------------------------')
        mem = SchedItems()
        print(mem.columns)
        print(mem.get_titles())
        print('---------------------------')
        selected_table = int(selected_table)
        data['selected_table'] = selected_table
        data['headers'] = mem.get_titles()
        #data['records'] = mem.get_rows()
    return render_template('back_ground.html', **data)

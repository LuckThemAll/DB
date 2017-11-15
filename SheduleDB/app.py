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


def kostil(kostil2):
    if kostil2 == 'AUDIENCES':
        return Audiences()

    if kostil2 == 'GROUPS':
        return Groups()

    if kostil2 == 'LESSONS':
        return Lessons()

    if kostil2 == 'LESSON_TYPES':
        return LessonTypes()

    if kostil2 == 'SCHED_ITEMS':
        return SchedItems()

    if kostil2 == 'SUBJECTS':
        return Subjects()

    if kostil2 == 'SUBJECT_GROUP':
        return SubjectGroup()

    if kostil2 == 'SUBJECT_TEACHER':
        return SubjectTeacher()

    if kostil2 == 'TEACHERS':
        return Teachers()

    if kostil2 == 'WEEKDAYS':
        return WeekDays()


@app.route('/')
def index():
    data = {}
    tables = get_tables()
    data['tables'] = tables
    selected_table = request.args.get('tables', '')
    if (selected_table.isdigit() and int(selected_table) >= 0 and int(selected_table) < len(tables)):

        selected_table = int(selected_table)
        mem = kostil(tables[selected_table])
        data['selected_table'] = selected_table
        data['headers'] = mem.get_titles()
        data['records'] = mem.get_rows()
    return render_template('back_ground.html', **data)

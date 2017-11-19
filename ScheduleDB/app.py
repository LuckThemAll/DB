from flask import Flask
from flask import request
from flask import render_template
from models import *

app = Flask(__name__)

tables_dict = {
          'AUDIENCES': Audiences(),
          'GROUPS': Groups(),
          'LESSONS': Lessons(),
          'LESSON_TYPES': LessonTypes(),
          'SCHED_ITEMS': SchedItems(),
          'SUBJECTS': Subjects(),
          'SUBJECT_GROUP': SubjectGroup(),
          'SUBJECT_TEACHER': SubjectTeacher(),
          'TEACHERS': Teachers(),
          'WEEKDAYS': WeekDays()
         }


@app.route('/')
def index():
    data = {}
    data['tables'] = [tables_dict[table].title for table in tables_dict]
    selected_table = request.args.get('tables', '')
    if (selected_table.isdigit() and int(selected_table) >= 0 and int(selected_table) < len(tables_dict)):
        selected_table = int(selected_table)
        tables = [item for item in tables_dict]
        print(tables)
        table = tables_dict[tables[selected_table]]
        print((table.get_rows()))
        data['selected_table'] = selected_table
        data['headers'] = table.get_titles()
        data['records'] = table.get_rows()
    return render_template('back_ground.html', **data)

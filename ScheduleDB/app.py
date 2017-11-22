from flask import Flask
from flask import request
from flask import render_template
from sqlBuilred import *
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
    selected_table_index = request.args.get('tables', '')
    search_str = request.args.get('sub_search', '')
    selected_col_name_index = request.args.get('search_col', '')
    if selected_col_name_index == '':
        selected_col_name_index = 0
    if (selected_table_index.isdigit() and int(selected_table_index) >= 0 and int(selected_table_index) < len(tables_dict)):
        selected_table = int(selected_table_index)
        selected_col_name_index = int(selected_col_name_index)
        data['search_str'] = search_str
        data['selected_table_index'] = selected_table
        tables_list = [item for item in tables_dict]
        selected_table = tables_dict[tables_list[selected_table]]
        cols_list = [item for item in selected_table.__dict__['columns']]
        if selected_col_name_index >= cols_list.__len__():
            selected_col_name_index = 0
        data['selected_col_name_index'] = selected_col_name_index
        selected_col_name = selected_table.columns[cols_list[selected_col_name_index]].get_title()
        data['selected_col_name'] = selected_col_name
        data['search_tables'] = [selected_table.columns[item].get_title() for item in selected_table.__dict__['columns']]
        data['headers'] = selected_table.get_titles()
        selected_table.get_rows((cols_list[selected_col_name_index], search_str))
        data['records'] = selected_table.get_rows((cols_list[selected_col_name_index], search_str))
    return render_template('back_ground.html', **data)

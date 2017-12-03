from flask import Flask
from flask import request
from flask import render_template
from sqlBuilred import *
from models import *

app = Flask(__name__)

tables = (
          Audiences(),
          Groups(),
          Lessons(),
          LessonTypes(),
          SchedItems(),
          Subjects(),
          SubjectGroup(),
          SubjectTeacher(),
          Teachers(),
          WeekDays()
        )


@app.route('/<int:selected_table_index>/')
@app.route('/')
def index(selected_table_index=0):
    data = {}
    data['tables'] = tables
    data['selected_col_name_index'] = request.args.get('search_col', 0, type=int)
    data['search_str'] = request.args.get('search_str', '')

    if 0 <= selected_table_index < len(tables):

        data['selected_table_index'] = selected_table_index

        selected_table = tables[selected_table_index]
        data['search_tables'] = [selected_table.columns[item].get_col_title() for item in selected_table.columns]
        data['headers'] = selected_table.get_titles()

        if data['search_str'] != '':
            search_col_names = [item for item in selected_table.columns]
            data['records'] = selected_table.fetch_all_by_params((search_col_names[data['selected_col_name_index']], ),
                                                                 (data['search_str'], ))
        else:
            data['records'] = selected_table.fetch_all()
        return render_template('main.html', **data)

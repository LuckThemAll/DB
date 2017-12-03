from flask import Flask
from flask import render_template
from flask import request
from models import *

app = Flask(__name__)


class SearchParameters:
    def __init__(self, table):
        self.search_col_names = [table.columns[item].get_col_title() for item in table.columns]
        self.params_count = request.args.get('params_count', 1, type=int)
        self.selected_col_name_indexes = request.args.getlist('search_col')
        self.search_params = request.args.getlist('search_param')
        self.operators = request.args.getlist('operator')


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

operators = {
    'СОДЕРЖИТ': 'CONTAINING',
    'РАВНО': '=',
    '>': '>',
    '>=': '>=',
    '<': '<',
    '<=': '<='
}


@app.route('/<int:selected_table_index>/')
@app.route('/')
def index(selected_table_index=0):
    data = {}
    data['tables'] = tables
    data['selected_col_name_index'] = request.args.get('search_col', 0, type=int)
    data['search_str'] = request.args.get('search_param', '')

    if 0 <= selected_table_index < len(tables):

        data['selected_table_index'] = selected_table_index

        selected_table = tables[selected_table_index]
        data['search_data'] = SearchParameters(selected_table)
        data['operators'] = [item for item in operators.keys()]
        for item in data['search_data'].__dict__.items():
            print(item)
        data['search_tables'] = [selected_table.columns[item].get_col_title() for item in selected_table.columns]
        data['headers'] = selected_table.get_titles()

        if data['search_data'].search_params:
            search_col_names = [item for item in selected_table.columns]
            ops = [operators[item] for item in data['search_data'].operators]
            data['records'] = selected_table.fetch_all_by_params([search_col_names[int(item)] for item in data['search_data'].selected_col_name_indexes],
                                                                 data['search_data'].search_params,
                                                                 ops)
        else:
            data['records'] = selected_table.fetch_all()
        return render_template('main.html', **data)

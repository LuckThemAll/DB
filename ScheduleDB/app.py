from flask import Flask
from flask import render_template
from models import *
from flask import request
from werkzeug.urls import url_encode
from math import ceil

app = Flask(__name__)


class SearchParameters:
    def __init__(self, table):
        self.search_col_names = [table.columns[item].get_col_title() for item in table.columns]
        self.params_count = request.args.get('params_count', 1, type=int)
        self.selected_col_name_indexes = request.args.getlist('search_col')
        self.search_params = request.args.getlist('search_param')
        self.operators = request.args.getlist('operator')
        self.sort_by_col = request.args.get('sort_by_col', 0)


class Paging:
    def __init__(self, records):
        self.recs_on_page = int(request.args.get('recs_on_page', 5))
        self.recs_count = len(records)
        self.pages_count = int(ceil(self.recs_count / self.recs_on_page))
        self.current_page = request.args.get('current_page', 1, type=int)
        if self.current_page not in range(self.pages_count):
            self.page = 1

    def select_recs(self, records):
        start = (self.current_page - 1) * self.recs_on_page
        return [records[i] for i in range(start + self.recs_on_page) if start <= i < len(records)]


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


@app.template_global()
def change_arg(arg, val):
    args = request.args.copy()
    args[arg] = val
    return '{}?{}'.format(request.path, url_encode(args))


@app.route('/<int:selected_table_index>/')


@app.route('/')
def index(selected_table_index=0):
    data = {}
    data['tables'] = tables

    if 0 <= selected_table_index < len(tables):

        data['selected_table_index'] = selected_table_index

        selected_table = tables[selected_table_index]
        data['search_data'] = SearchParameters(selected_table)
        data['operators'] = [item for item in operators.keys()]

        data['search_tables'] = [selected_table.columns[item].get_col_title() for item in selected_table.columns]
        data['headers'] = selected_table.get_titles()

        search_col_names = [item for item in selected_table.columns]
        sort_by_col_name = search_col_names[int(data['search_data'].sort_by_col)]
        if data['search_data'].search_params:
            ops = [operators[item] for item in data['search_data'].operators]
            data['records'] = selected_table.fetch_all_by_params(
                [search_col_names[int(item)] for item in data['search_data'].selected_col_name_indexes],
                data['search_data'].search_params,
                ops,
                sort_by_col_name)
            data['paging'] = Paging(data['records'])
            data['records'] = data['paging'].select_recs(data['records'])

        else:
            data['records'] = selected_table.fetch_all(sort_by_col_name)
            data['paging'] = Paging(data['records'])
            data['records'] = data['paging'].select_recs(data['records'])
        return render_template('main.html', **data)

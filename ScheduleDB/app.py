from flask import Flask
from flask import render_template
from models import *
from flask import request
from werkzeug.urls import url_encode
from math import ceil

app = Flask(__name__)


class SearchParameters:
    def __init__(self, table):
        self.search_col_names = [getattr(table.columns, item).get_col_title() for item in table.columns.__dict__]
        self.params_count = request.args.get('params_count', 1, type=int)
        self.selected_col_name_indexes = request.args.getlist('search_col')
        self.search_params = request.args.getlist('search_param')
        self.operators = request.args.getlist('operator')
        self.sort_by_col = request.args.get('sort_by_col', 0)


class Paging:
    def __init__(self, records):
        self.recs_on_page = request.args.get('recs_on_page', 5, type=int)
        self.recs_count = len(records)
        self.pages_count = int(ceil(self.recs_count / self.recs_on_page))
        self.current_page = request.args.get('current_page', 1, type=int)
        if self.current_page not in range(self.pages_count):
            self.page = 1

    def select_recs(self, records):
        start = (self.current_page - 1) * self.recs_on_page
        return [records[i] for i in range(start + self.recs_on_page) if start <= i < len(records)]


class TemplateData:
    def __init__(self):
        self.tables = tables


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


@app.route('/')
def start():
    data = TemplateData()
    return render_template('start_page.html', **data.__dict__)


@app.route('/<int:selected_table_index>/')
def index(selected_table_index=0):
    data = TemplateData()

    if 0 <= selected_table_index < len(tables):

        data.selected_table_index = selected_table_index

        selected_table = tables[selected_table_index]
        data.search_data = SearchParameters(selected_table)
        data.operators = [item for item in operators.keys()]
        print(selected_table.columns)
        data.search_tables = [selected_table.columns.get_col(item).get_col_title() for item in selected_table.columns.__dict__]
        data.headers = selected_table.columns.get_titles()

        search_col_names = [item for item in selected_table.columns.__dict__]
        sort_by_col_name = search_col_names[int(data.search_data.sort_by_col)]
        if data.search_data.search_params:
            ops = [operators[item] for item in data.search_data.operators]
            recs = data.records = selected_table.fetch_all_by_params(
                [search_col_names[int(item)] for item in data.search_data.selected_col_name_indexes],
                data.search_data.search_params,
                ops,
                sort_by_col_name)
            p = data.paging = Paging(recs)
            data.records = p.select_recs(recs)

        else:
            recs = data.records = selected_table.fetch_all(sort_by_col_name)
            data.paging = Paging(recs)
            data.records = data.paging.select_recs(recs)
        return render_template('main.html', **data.__dict__)


@app.route('/<int:selected_table_index>/add')
def add_record(selected_table_index=0):
    data = TemplateData()
    data.selected_table_index = selected_table_index
    selected_table = tables[selected_table_index]
    data.titles = selected_table.columns.get_titles_without_id()
    data.options = {}
    for key, val in selected_table.columns.__dict__.items():
        if isinstance(val, ReferenceField):
            sql = SQLBuilder(selected_table.columns.get_col(key).source)
            sql.clear_fields()
            sql.set_fields('name')
            sql.set_from_table()
            sql.add_l_joins()
            cur.execute(sql.get_sql())
            data.options[key] = cur.fetchall()
        elif key != 'id':
            data.options[key] = 'none'
    all_fields_correct = True
    params = request.args.getlist("p")
    for item in request.args.getlist("p"):
        if not item:
            all_fields_correct = False
            break

    if len(params) != 0:
        for i, col in enumerate(selected_table.columns.get_cols_without_id()):
            if isinstance(selected_table.columns.get_col(col), ReferenceField):
                print(selected_table.columns.get_col(col))
                atr_name = selected_table.columns.get_col(col).get_col_name(selected_table.table_name)
                atr_table = selected_table.columns.get_col(col).get_source_table()
                idd = selected_table.columns.get_col(col).get_source_col_id()
                sql = 'select {2} from {1} where {0}=?'.format(atr_name, atr_table, idd)
                cur.execute(sql, (params[i],))
                params[i] = int(cur.fetchall()[0][0])

    if all_fields_correct and len(params) != 0:
        sql = SQLBuilder(selected_table)
        cur.execute(sql.set_insert(selected_table.columns.get_cols_without_id()), params)
    return render_template('add.html', **data.__dict__)


@app.route('/<int:selected_table_index>/modify/<int:rec_id>')
def modify(selected_table_index=0, rec_id=0):
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    data = TemplateData()
    data.id = rec_id
    data.selected_table_index = selected_table_index
    selected_table = tables[selected_table_index]
    data.titles = selected_table.columns.get_titles_without_id()
    data.current_values = {}

    data.options = {}
    for key, val in selected_table.columns.__dict__.items():
        if isinstance(val, ReferenceField):
            sql = SQLBuilder(selected_table.columns.get_col(key).source)
            sql.clear_fields()
            sql.set_fields('name')
            sql.set_from_table()
            sql.add_l_joins()
            cur.execute(sql.get_sql())
            data.options[key] = cur.fetchall()
        elif key != 'id':
            sqll = 'select {0}.{1} from {0} where {0}.id = ?'.format(selected_table.table_name, 'name')
            cur.execute(sqll, get_list(rec_id))
            data.options[key] = 'none'
    print('options----------', data.options)

    # Сохранение текущих значений
    for key, val in selected_table.columns.__dict__.items():
        if isinstance(val, ReferenceField):
            sql = SQLBuilder(selected_table.columns.get_col(key).source)
            select_col_id = 'select {0}.{1} from {0} where {0}.id = ?'.format(selected_table.table_name,
                                                                              selected_table.columns.get_col(key).col_name)
            cur.execute(select_col_id, get_list(data.id))
            col_id = cur.fetchone()
            sql.clear_fields()
            sql.set_fields('name')
            sql.set_from_table()
            sql.add_l_joins()
            sql.add_where_col_names('id')
            sql.add_operators('=')
            print(sql.get_sql(), get_list(col_id))
            cur.execute(sql.get_sql(), col_id)
            col_name = cur.fetchall()
            print(col_name)
            if len(col_name) > 0:
                data.current_values[key] = col_name
            else:
                data.current_values[key] = 'none'
        elif key != 'id':
            sql = SQLBuilder(selected_table)
            sql.clear_fields()
            sql.set_fields(key)
            sql.set_from_table()
            sql.add_where_col_names('id')
            sql.add_operators('=')
            cur.execute(sql.get_sql(), (data.id,))
            data.current_values[key] = cur.fetchall()
    print('current_values----------', data.current_values)

    all_fields_correct = True
    params = request.args.getlist("p")
    for item in request.args.getlist("p"):
        if not item:
            all_fields_correct = False
            break
    print('params----------', params)
    mem = []
    if len(params) != 0:
        for i, col in enumerate(selected_table.columns.get_cols_without_id()):
            if isinstance(col, ReferenceField):
                print(selected_table.columns.get_col(col).get_col_name(selected_table.table_name))
                atr_name = selected_table.columns.get_col(col).get_col_name(selected_table.table_name)
                if isinstance(selected_table.columns.get_col(col), ReferenceField):
                    atr_table = selected_table.columns.get_col(col).get_source_table()
                    idd = selected_table.columns.get_col(col).get_source_col_id()
                else:
                    atr_table = selected_table.table_name
                    idd = rec_id
                sql = 'select {2} from {1} where {0}=?'.format(atr_name, atr_table, idd)
                print(sql)
                cur.execute(sql, (params[i],))
                mem.append(cur.fetchall()[0][0])

    if all_fields_correct and len(params) != 0:
        sql = SQLBuilder(selected_table)
        cols = selected_table.columns.get_cols_without_id()
        print(cols, mem)
        mem.append(rec_id)
        params.append(rec_id)
        print(sql.set_update(cols), params)
        if len(mem) != 1:
            print('111111111111111111111', mem, len(mem))
            cur.execute(sql.set_update(cols), mem)
        else:
            print('222222222222222222222')
            cur.execute(sql.set_update(cols), params)



    cur.transaction.commit()

    # Сохранение текущих значений
    for key, val in selected_table.columns.__dict__.items():
        if isinstance(val, ReferenceField):
            sql = SQLBuilder(selected_table.columns.get_col(key).source)
            select_col_id = 'select {0}.{1} from {0} where {0}.id = ?'.format(selected_table.table_name,
                                                                              selected_table.columns.get_col(
                                                                                  key).col_name)
            cur.execute(select_col_id, get_list(data.id))
            col_id = cur.fetchone()
            sql.clear_fields()
            sql.set_fields('name')
            sql.set_from_table()
            sql.add_l_joins()
            sql.add_where_col_names('id')
            sql.add_operators('=')
            print(sql.get_sql(), get_list(col_id))
            cur.execute(sql.get_sql(), col_id)
            col_name = cur.fetchall()
            print(col_name)
            if len(col_name) > 0:
                data.current_values[key] = col_name
            else:
                data.current_values[key] = 'none'
        elif key != 'id':
            sql = SQLBuilder(selected_table)
            sql.clear_fields()
            sql.set_fields(key)
            sql.set_from_table()
            sql.add_where_col_names('id')
            sql.add_operators('=')
            cur.execute(sql.get_sql(), (data.id,))
            data.current_values[key] = cur.fetchall()

    return render_template('modify.html', **data.__dict__)

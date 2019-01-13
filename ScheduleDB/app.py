from flask import Flask
from flask import render_template
from flask import request
from werkzeug.urls import url_encode
from math import ceil
from conflicts import *
import password_encoder

app = Flask(__name__)


class SearchParameters:
    def __init__(self, table):
        self.search_col_names = [getattr(table.columns, item).get_col_title() for item in table.columns.__dict__]
        self.params_count = request.args.get('params_count', 0, type=int)
        self.selected_col_name_indexes = request.args.getlist('search_col')
        self.search_params = request.args.getlist('search_param')
        self.operators = request.args.getlist('operator')


class Paging:
    def __init__(self, records):
        self.recs_on_page = request.args.get('recs_on_page', 5, type=int)
        self.recs_count = len(records)
        self.pages_count = int(ceil(self.recs_count / self.recs_on_page))
        self.current_page = request.args.get('current_page', 1, type=int)
        if self.current_page not in range(self.pages_count + 1):
            self.current_page = 1

    def select_recs(self, records):
        start = (self.current_page - 1) * self.recs_on_page
        return [records[i] for i in range(start + self.recs_on_page) if start <= i < len(records)]


class TemplateData:
    def __init__(self):
        self.tables = tables
        self.table = None
        self.login = ''


operators = {
    'СОДЕРЖИТ': 'CONTAINING',
    'РАВНО': '=',
    'НЕ РАВНО': '!=',
    '>': '>',
    '>=': '>=',
    '<': '<',
    '<=': '<='
}

logic_operators = ('AND', 'OR')


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
        data.delId = request.args.get('delid', -1, type=int)
        if data.delId != -1:
            sql = SQLBuilder(selected_table)
            cur.execute(sql.get_delete(), get_list(data.delId))
            data.delId = -1

        data.sort_by_col = request.args.get('sort_by_col', 0)
        data.sort_type = request.args.get('sort_type', 'inc', type=str)
        data.logic_operator = request.args.get('lo', 'and')

        data.logic_operators = logic_operators
        data.search_data = SearchParameters(selected_table)
        data.operators = [item for item in operators.keys()]
        data.search_tables = [selected_table.columns.get_col(item).get_col_title() for item in
                              selected_table.columns.__dict__]
        data.headers = selected_table.columns.get_titles()

        search_col_names = [item for item in selected_table.columns.__dict__]

        sort_by_col_name = search_col_names[int(data.sort_by_col)]
        if data.search_data.search_params:
            ops = [operators[item] for item in data.search_data.operators]
            recs = data.records = selected_table.fetch_all_by_params(
                [search_col_names[int(item)] for item in data.search_data.selected_col_name_indexes],
                data.search_data.search_params,
                ops,
                data.logic_operator,
                sort_by_col_name,
                data.sort_type)
            p = data.paging = Paging(recs)
            data.records = p.select_recs(recs)

        else:
            recs = data.records = selected_table.fetch_all_names(sort_by_col_name, data.sort_type)
            data.paging = Paging(recs)
            data.records = data.paging.select_recs(recs)
        return render_template('main.html', **data.__dict__)


def get_all_options(data):
    columns = data.table.columns
    result = {}
    for i, col in enumerate(data.table.columns.__dict__):
        if type(columns.get_col(col)) is ReferenceField:
            sql = SQLBuilder.get_options(
                columns.get_col(col).source.table_name,
                columns.get_col(col).get_col_name(data.table.table_name))
            result[col] = {}
            result[col]['val'] = {}
            for row in cur.execute(sql):
                result[col]['val'][row[0]] = row[1]
                result[col]['index'] = i - 1
        elif col != 'id':
            result[col] = None
    return result


def correct_values(values):
    for i, item in enumerate(values):
        if item == '':
            values[i] = None


@app.route('/<int:selected_table_index>/add/')
def add_record(selected_table_index=0):
    data = TemplateData
    data.f_olap_col = request.args.get('col', None, type=int)
    data.f_olap_row = request.args.get('row', None, type=int)
    data.f_olap_col_val = request.args.get('col_value', None, type=str)
    data.f_olap_row_val = request.args.get('row_value', None, type=str)
    data.table = tables[selected_table_index]
    data.values = data.table.fetch_all()
    data.titles = data.table.columns.get_titles_without_id()
    data.options = get_all_options(data)
    new_values = request.args.getlist("p")
    correct_values(new_values)
    if is_correct_fields(new_values):
        sql = SQLBuilder(data.table)
        cur.execute(sql.get_insert(data.table.columns.get_cols_without_id()), new_values)
    cur.transaction.commit()
    update_conflicts()
    return render_template('add.html', **data.__dict__)


@app.route('/<int:selected_table_index>/modify/<int:rec_id>/')
def modify(selected_table_index=0, rec_id=0):
    data = TemplateData
    data.table = tables[selected_table_index]
    data.values = data.table.fetch_all()
    data.titles = data.table.columns.get_titles_without_id()
    data.options = get_all_options(data)
    data.current_values = data.table.fetch_one(rec_id)
    new_values = request.args.getlist("p")
    correct_values(new_values)
    if is_correct_fields(new_values):
        sql = SQLBuilder(data.table)
        cols = data.table.columns.get_cols_without_id()
        new_values.append(rec_id)
        cur.execute(sql.get_update(cols), new_values)
        data.current_values = data.table.fetch_one(rec_id)
    cur.transaction.commit()
    update_conflicts()
    return render_template('modify.html', **data.__dict__)


@app.route('/schedule/dad/<int:rec_id>/')
def drop(rec_id=0):
    table = SchedItems()
    cols = table.columns.get_cols_without_id()
    vals = []
    [vals.append(item) for item in table.fetch_one(rec_id)]
    x_proj = request.args.get("x_proj")
    y_proj = request.args.get("y_proj")
    new_x_proj = request.args.get("new_x_proj")
    new_y_proj = request.args.get("new_y_proj")
    vals[int(x_proj)] = new_x_proj
    vals[int(y_proj)] = new_y_proj
    vals.append(rec_id)
    s = SQLBuilder(table)
    for i in range(vals.__len__()):
        if vals[i] == "null":
            vals[i] = None
    cur.execute(s.get_update(cols), vals)
    cur.transaction.commit()
    update_conflicts()
    return '1'


@app.route('/schedule/')
def view_schedule():
    data = TemplateData()
    table = SchedItems()

    data.delId = request.args.get('delid', -1, type=int)
    if data.delId != -1:
        sql = SQLBuilder(table)
        cur.execute(sql.get_delete(), get_list(data.delId))
        update_conflicts()
        data.delId = -1

    data.projections = {}
    for i, item in enumerate(table.columns.get_cols_without_id()):
        data.projections[i] = table.columns.get_col(item).col_title

    data.sel_y = request.args.get('y', 0, type=int)
    data.sel_x = request.args.get('x', 6, type=int)

    meta = []
    [meta.append(item) for item in table.columns.__dict__]
    meta.pop(0)
    rows = table.columns.get_col(meta[data.sel_x]).source.fetch_all('ID', 'NAME')
    rows.append((None, None))
    cols = table.columns.get_col(meta[data.sel_y]).source.fetch_all('ID', 'NAME')
    cols.append((None, None))

    viewed_table = dict.fromkeys([(col[1], col[0]) for col in cols])
    for col in viewed_table:
        viewed_table[col] = dict.fromkeys([(row[1], row[0]) for row in rows])

    data.search_col_names = [item for item in table.columns.__dict__]
    data.search_data = SearchParameters(table)
    data.logic_operator = None
    data.sort_type = None

    rows_name = []
    rows_id = []
    s = SQLBuilder(table)
    s.set_schedule_view()
    data.logic_operator = request.args.get('lo', 'and')
    data.p_change_flag = request.args.get('p_change_flag', 'true', type=str)
    data.header_view = request.args.get('header_view', 'true')
    data.operators = operators

    data.showed_cols = request.args.getlist('shw_cls')

    if data.p_change_flag == 'true':
        data.showed_cols = []
        [data.showed_cols.append(item) for item in data.search_data.search_col_names]
        if data.sel_y != data.sel_x:
            del data.showed_cols[max(data.sel_y + 1, data.sel_x + 1)]
            del data.showed_cols[min(data.sel_y + 1, data.sel_x + 1)]
        else:
            del data.showed_cols[data.sel_y]

    data.search_data = SearchParameters(table)
    if data.search_data.search_params:
        a = []
        for item in table.columns.__dict__:
            a.append(item)
        col_names = []
        for item in data.search_data.selected_col_name_indexes:
            col_names.append(a[int(item) - 1])
        s.add_logic_operator('OR')
        data.operators = [item for item in operators.keys()]
        ops = [operators[item] for item in data.search_data.operators]
        s.add_operators(ops)
        s.add_where_col_names(col_names)
        cur.execute(s.get_sql(), get_list(data.search_data.search_params))
    else:
        cur.execute(s.get_sql())
    rows = cur.fetchall()
    for row in rows:
        rows_name.append([])
        rows_id.append([row[0]])
        for i in range(len(row)):
            rows_name[-1].append(row[i]) if i == 0 or i % 2 else rows_id[-1].append(row[i])

    for i in range(len(rows_name)):
        for j in range(len(rows_name[i])):
            rows_name[i][j] = (rows_name[i][j], rows_id[i][j])

    rows = rows_name
    for row in rows:
        if viewed_table[row[data.sel_y + 1]][row[data.sel_x + 1]] is None:
            viewed_table[row[data.sel_y + 1]][row[data.sel_x + 1]] = [row]
        else:
            viewed_table[row[data.sel_y + 1]][row[data.sel_x + 1]].append(row)

    data.col_indexes = []
    [data.col_indexes.append(i) for i in range(data.projections.__len__())]

    data.viewed_table = viewed_table
    query = SQLBuilder.get_conflicting_ids()
    cur.execute(query)
    data.conflictingIDs = [item[0] for item in cur.fetchall()]
    return render_template('schedule.html', **data.__dict__)


@app.route("/conflicts/")
@app.route("/conflicts/<int:type_id>/")
def conflict(type_id=0):
    data = TemplateData()
    data.table = SchedItems()
    data.viewedNames = data.table.columns.get_titles()
    data.delId = request.args.get('delID', -1, type=int)
    if data.delId != -1:
        sql = SQLBuilder(data.table)
        try:
            cur.execute(sql.get_delete(), get_list(data.delId))
            data.delId = -1
            update_conflicts()
        except:
            data.delId = -1
    query = SQLBuilder.get_conflict(SQLBuilder(SchedItems()), type_id)
    print(query)
    cur.execute(query)
    data.rows = cur.fetchall()
    data.conflicts_by_groups = [[]]
    data.last_group_id = -1
    for conflict in data.rows:
        if conflict == data.rows[0]:
            data.last_group_id = conflict[0]
        if conflict[0] != data.last_group_id:
            data.conflicts_by_groups.append([])
        data.conflicts_by_groups[-1].append(conflict[1:])
        data.last_group_id = conflict[0]
    data.rows_list = data.conflicts_by_groups
    data.conflicts = conflicts
    return render_template("conflicts_page.html", **data.__dict__)


@app.route("/registration/")
def authentication():
    data = TemplateData()
    if request.method == 'GET':
        return render_template("registration.html", **data.__dict__)
    data.login = request.args.get("login", "", type=str)
    enc = password_encoder.encoder(request.args.get("password", "", type=str))
    # user =
    return render_template("registration.html", **data.__dict__)

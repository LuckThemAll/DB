from fields import *
from misc import *


class SQLBuilder:
    fields = []
    l_joins = []
    where_col_names = []
    operators = []
    logic_operator = ''
    sort_by_col = ''
    from_table = ''
    sql = ''
    sort_type = 'inc'

    def __init__(self, table):
        self.table = table
        self.table_name = self.table.table_name

    def clear_fields(self):
        self.fields = []
        self.l_joins = []
        self.where_col_names = []
        self.operators = []
        self.sort_by_col = ''
        self.from_table = ''
        self.sql = ''
        self.logic_operator = ''
        self.sort_type = 'inc'

    def set_fields(self, *fields, name=True):
        if not fields:
            [self.fields.append(col) for col in self.table.columns.get_col_names(self.table_name)]
        else:
            if type(fields[0]) is list:
                fields = fields[0]
            if name:
                [self.fields.append(self.table.columns.get_col(field).get_col_name(self.table_name)) for field in fields]
            else:
                [self.fields.append(self.table_name + '.' + field) for field in fields]

    def set_from_table(self):
        self.from_table = 'from ' + self.table_name + ' '

    def add_l_joins(self):
        [self.l_joins.append((val.source.table_name, val.ref, self.table_name, key))
            for key, val in self.table.columns.__dict__.items()
            if isinstance(val, ReferenceField)
         ]

    def add_where_col_names(self, col_names):
        col_names = get_list(col_names)
        [self.where_col_names.append(self.table.get_tab_col(col_name)) for col_name in col_names]

    def add_operators(self, operators):
        operators = get_list(operators)
        [self.operators.append(operator) for operator in operators]

    def add_sort_by_col(self, sort_by_col):
        self.sort_by_col = self.table.get_tab_col_for_sort(sort_by_col)

    def get_sql(self):
        self.sql = 'select ' + ','.join(self.fields) + ' '

        self.sql += 'from ' + self.table_name + ' '

        if self.l_joins:
            for l_join in self.l_joins:
                self.sql += 'left join {0} on {0}.{1}={2}.{3} '.format(*l_join)

        if self.where_col_names:
            self.sql += 'where '
            for i, where_col_name in enumerate(self.where_col_names):
                self.sql += '{0} {1} ? '.format(where_col_name, self.operators[i])
                if i < self.where_col_names.__len__() - 1:
                    self.sql += self.logic_operator + ' '

        if self.sort_by_col:
            self.sql += 'order by {0} '.format(self.sort_by_col)
            if self.sort_type == 'desc':
                self.sql += 'desc'
        return self.sql

    def get_insert(self, fields, table=None, data=None, is_conflict = False):
        if not is_conflict:
            sql = 'INSERT INTO {0}({1}) VALUES ({2});'.format(self.table_name, ','.join(fields), ','.join('?'*len(fields)))
            return sql
        else:
            sql = 'insert into %s ' % table
            sql += '(%s) ' % ','.join(field for field in data)
            sql += 'values (?%s)' % (',?' * (len(data) - 1))
            return sql

    def get_update(self, cols):
        updated_cols = []
        for i, col in enumerate(cols):
            updated_cols.append(col + '=' + '? ')
        sql = 'UPDATE {0} SET {1} WHERE {0}.ID=?'.format(self.table_name, ','.join(updated_cols))
        return sql

    def get_delete(self):
        sql = 'DELETE FROM {0} WHERE {0}.ID = ?'.format(self.table_name)
        return sql

    def add_logic_operator(self, logic_operator):
        self.logic_operator = logic_operator

    def add_sort_type(self, sort_type):
        self.sort_type = sort_type

    def get_conflict(self, type_id):
        self.clear_fields()
        self.set_fields()
        sql = 'select c.CONFLICT_GROUP_ID, '+', '.join(self.fields) + ' from CONFLICTS c '
        sql += ' inner join SCHED_ITEMS on c.SCHED_ITEM_ID = SCHED_ITEMS.ID '
        self.add_l_joins()
        for l_join in self.l_joins:
            sql += ' left join {0} on {0}.{1}={2}.{3} '.format(*l_join)
        sql += ' where c.CONFLICT_TYPE_ID = %d' % type_id
        self.clear_fields()
        return sql

    def get_conflicting_ids(self):
        sql = 'SELECT c.SCHED_ITEM_ID FROM CONFLICTS c'
        return sql

    def create_conflict(self, fields):
        sql = 'select ID,'
        sql += ','.join('t1.' + field for field in fields)
        sql += ' from SCHED_ITEMS t1 where exists (select * from SCHED_ITEMS t2 where '
        sql += ' AND '.join('t1.%s = t2.%s' % (field, field) for field in fields)
        sql += ' AND t1.ID <> t2.ID)'
        sql += ' GROUP BY %s,ID' % ','.join(fields)
        return sql

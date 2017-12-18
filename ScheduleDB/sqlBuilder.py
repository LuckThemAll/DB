from fields import *
from misc import *


class SQLBuilder:
    fields = []
    l_joins = []
    where_col_names = []
    operators = []
    sort_by_col = ''
    from_table = ''
    sql = ''

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

    def set_fields(self, *fields, name=True):
        if not fields:
            [self.fields.append(col) for col in self.table.columns.get_col_names(self.table_name)]
        else:
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
                    self.sql += 'and '

        if self.sort_by_col:
            self.sql += 'order by {0} '.format(self.sort_by_col)

        return self.sql

    def set_insert(self, fields):
        sql = 'INSERT INTO {0}({1}) VALUES ({2});'.format(self.table_name, ','.join(fields), ','.join('?'*len(fields)))
        return sql

    def set_update(self, cols):
        updated_cols = []
        for i, col in enumerate(cols):
            updated_cols.append(col + '=' + '? ')
        sql = 'UPDATE {0} SET {1} WHERE {0}.ID=?'.format(self.table_name, ','.join(updated_cols))
        return sql

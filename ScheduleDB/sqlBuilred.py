from fields import *


class SQLBuilder:
    fields = []
    l_joins = []
    where_col_names = []
    from_table = ''
    sql = ''

    def __init__(self, table):
        self.table = table
        self.table_name = self.table.table_name

    def set_fields(self):
        self.fields = []
        for col in self.table.get_col_names():
            self.fields.append(col)

    def set_from_table(self):
        self.from_table = 'from ' + self.table_name + ' '

    def add_l_joins(self):
        self.l_joins = []
        for key, val in self.table.columns.items():
            if isinstance(val, ReferenceField):
                self.l_joins.append((val.source.table_name, val.ref, self.table_name, key))

    def add_where_col_names(self, col_names):
        self.where_col_names = []
        for col_name in col_names:
            self.where_col_names.append(self.table.get_tab_col(col_name))

    def get_sql(self):
        self.sql = 'select '
        if self.fields:
            for i, field in enumerate(self.fields):
                if i == 0:
                    self.sql += field + ' '
                else:
                    self.sql += ', ' + field + ' '

        self.sql += 'from ' + self.table_name + ' '

        if self.l_joins:
            for l_join in self.l_joins:
                self.sql += 'left join {0} on {0}.{1}={2}.{3} '.format(l_join[0], l_join[1], l_join[2], l_join[3])

        if self.where_col_names:
            for where_col_name in self.where_col_names:
                self.sql += 'where {} containing ? '.format(where_col_name)

        return self.sql

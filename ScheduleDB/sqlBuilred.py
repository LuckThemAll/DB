from fields import *


class SQLBuilder:
    query = 'select '
    fields = []
    l_join = []
    where_param = []
    from_table = 'form '

    def __init__(self, table):
        self.table = table
        self.table_name = self.table.table_name

    def add_fields(self):
        for col in self.table.get_col_names():
            self.fields.append(col)

    def add_from_table(self):
        self.from_table += self.table_name + ' '

    def add_l_joins(self):
        for key, val in self.table.columns.items():
            if isinstance(val, ReferenceField):
                self.l_join.append((val.source.table_name, val.ref, self.table_name, key))

    def add_where(self, wheres):
        self.where_param.append(self.table.get_tab_col(wheres[0]))

    def get_sql(self):
        return self.query

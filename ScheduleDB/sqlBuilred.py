from fields import *


class SQLBuilder:
    def __init__(self, table):
        self.query = 'select '
        self.table = table
    pass

    def add_fields(self):
        for i, col in enumerate(self.table.get_col_names()):
            if i == 0:
                self.query += col
            else:
                self.query += ', ' + col
        self.query += ' '

    def add_from_table(self):
        self.query += 'from ' + self.table.table_name + ' '

    def add_l_joins(self):
        cols = self.table.columns
        refs_fields = (item for item in cols if type(cols[item]) is ReferenceField)
        for item in refs_fields:
            col = cols[item]
            self.query += ('left join {0} on {0}.{1}={2}.{3} '.format(col.source.table_name,
                                                                      col.ref,
                                                                      self.table.table_name,
                                                                      item))

    def add_where(self, wheres):
        self.query += 'where ' + self.table.get_tab_col(wheres[0]) + ' containing ? '

    def create_sql(self, wheres=()):
        self.add_fields()
        self.add_from_table()
        print([self.table.columns[item] for item in self.table.columns])
        for item in self.table.columns:
            if isinstance(self.table.columns[item], ReferenceField):
                self.add_l_joins()
                break
        if wheres[1]:
            self.add_where(wheres)

    def get_sql(self):
        return self.query

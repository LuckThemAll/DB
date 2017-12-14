from abc import *


class BaseField(metaclass=ABCMeta):
    def __init__(self, col_name, col_title):
        self.col_name = col_name
        self.col_title = col_title

    def get_col_name(self, table_name):
        return table_name + '.' + self.col_name

    def get_col_title(self):
        return self.col_title


class IntegerField(BaseField):
    def __init__(self, col_name, col_title):
        super().__init__(col_name, col_title)


class StringField(BaseField):
    def __init__(self, col_name, col_title):
        super().__init__(col_name, col_title)


class ReferenceField(BaseField):
    def __init__(self, col_name, col_title, ref, source, field):
        super().__init__(col_name, col_title)
        self.ref = ref
        self.source = source
        self.field = field

    def get_col_name(self, table_name):
        return self.source.table_name + '.' + self.field

    def get_source_col_id(self):
        return self.source.table_name + '.' + 'id'

    def get_source_table(self):
        return self.source.table_name

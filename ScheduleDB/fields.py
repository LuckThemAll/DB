from abc import *


class BaseField(metaclass=ABCMeta):
    def __init__(self, col_name, col_title, pixels):
        self.col_name = col_name
        self.col_title = col_title
        self.pixels = pixels

    def get_col_name(self):
        return self.col_name

    def get_col_title(self):
        return self.col_title


class IntegerField(BaseField):
    def __init__(self, col_name=None, col_title=None, pixels=20):
        super().__init__(col_name, col_title, pixels)


class StringField(BaseField):
    def __init__(self, col_name=None, col_title=None, pixels=20):
        super().__init__(col_name, col_title, pixels)


class ReferenceField(BaseField):
    def __init__(self, col_name, col_title, ref, source, field, pixels=100):
        super().__init__(col_name, col_title, pixels)
        self.ref = ref
        self.source = source
        self.field = field

    def get_col_title(self):
        return self.source.col_title

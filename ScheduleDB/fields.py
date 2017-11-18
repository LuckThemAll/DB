from abc import *


class NamedField(metaclass=ABCMeta):
    def __init__(self, col_name, title, pixels):
        self.col_name = col_name
        self.title = title
        self.pixels = pixels


class IntegerField(NamedField):
    def __init__(self, col_name=None, title=None, pixels=20):
        super().__init__(col_name, title, pixels)


class StringField(NamedField):
    def __init__(self, col_name=None, title=None, pixels=20):
        super().__init__(col_name, title, pixels)


class ReferenceField:
    def __init__(self, ref, source, field):
        self.ref = ref
        self.source = source
        self.field = field

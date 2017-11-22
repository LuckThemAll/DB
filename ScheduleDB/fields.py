from abc import *


class NamedField(metaclass=ABCMeta):
    def __init__(self, col_name, title, pixels):
        self.col_name = col_name
        self.title = title
        self.pixels = pixels

    def get_col_name(self):
        return self.__dict__['col_name']

    def get_title(self):
        return self.title

    @abstractmethod
    def type_check(self, item):
        pass


class IntegerField(NamedField):
    def __init__(self, col_name=None, title=None, pixels=20):
        super().__init__(col_name, title, pixels)

    def type_check(self, item):
        return type(item) is int


class StringField(NamedField):
    def __init__(self, col_name=None, title=None, pixels=20):
        super().__init__(col_name, title, pixels)

    def type_check(self, item):
        return type(item) is str


class ReferenceField:
    def __init__(self, ref, source, field):
        self.ref = ref
        self.source = source
        self.field = field

    def get_ref(self):
        return self.source

    def get_title(self):
        return self.source.title

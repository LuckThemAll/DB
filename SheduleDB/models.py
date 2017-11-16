from db_connect import cur
from abc import *


class BaseModel(metaclass=ABCMeta):
    def __init__(self, table_name=None):
        self.table_name = table_name
        self.columns = {}

    def add_property(self, property_type, name, *args):
        template = {'Integer': {'Type': property_type, 'col_name': args[0], 'title': args[1], 'pixels': args[2]},
                    'String': {'Type': property_type, 'col_name': args[0], 'title': args[1], 'pixels': args[2]},
                    'Reference': {'Type': property_type, 'ref': args[0], 'source': args[1], 'field': args[2]}
                    }
        self.columns[name] = template[property_type]

    def get_titles(self):
        return [self.columns[item]['title'] for item in self.columns]

    def get_rows(self):

        pass


class NamedModel(BaseModel):
    def __init__(self, table_name=None, title=None):
        super().__init__(table_name)
        self.add_property('Integer', 'id', 'ID', 'Ключ', 20)
        self.add_property('String', 'name', 'NAME', title, 200)


class RefModel(BaseModel):
    def __init__(self, table_name):
        super().__init__(table_name)

    def get_titles(self):
        return [self.columns[item]['source']().columns['name']['title'] for item in self.columns]


class Audiences(NamedModel):
    def __init__(self):
        super().__init__('AUDIENCES', 'Номер аудитории')


class Groups(NamedModel):
    def __init__(self):
        super().__init__('GROUPS', 'Группа')


class LessonTypes(NamedModel):
    def __init__(self):
        super().__init__('LESSON_TYPES', 'Вид занятия')


class Subjects(NamedModel):
    def __init__(self):
        super().__init__('SUBJECTS', 'Предмет')


class Teachers(NamedModel):
    def __init__(self):
        super().__init__('TEACHERS', 'ФИО')


class Lessons(NamedModel):
    def __init__(self):
        super().__init__('LESSONS', 'Номер пары')
        self.add_property('Integer', 'order_number', 'ORDER_NUMBER', 'Порядок', 20)


class WeekDays(NamedModel):
    def __init__(self):
        super().__init__('WEEKDAYS', 'День недели')
        self.add_property('Integer', 'order_number', 'ORDER_NUMBER', 'Порядок', 20)


class SubjectGroup(RefModel):
    def __init__(self):
        super().__init__('SUBJECT_GROUP')
        self.add_property('Reference', 'subject_id', 'ID', Subjects, 'NAME')
        self.add_property('Reference', 'group_id', 'ID', Groups, 'NAME')


class SubjectTeacher(RefModel):
    def __init__(self):
        super().__init__('SUBJECT_TEACHER')
        self.add_property('Reference', 'subject_id', 'ID', Subjects, 'NAME')
        self.add_property('Reference', 'teacher_id', 'ID', Teachers, 'NAME')


class SchedItems(RefModel):
    def __init__(self):
        super().__init__('SCHED_ITEM')
        self.add_property('Reference', 'lesson_id', 'ID', Lessons, 'NAME')
        self.add_property('Reference', 'subject_id', 'ID', Subjects, 'NAME')
        self.add_property('Reference', 'audience_id', 'ID', Audiences, 'NAME')
        self.add_property('Reference', 'group_id', 'ID', Groups, 'NAME')
        self.add_property('Reference', 'teacher_id', 'ID', Teachers, 'NAME')
        self.add_property('Reference', 'type_id', 'ID', LessonTypes, 'NAME')
        self.add_property('Reference', 'weekday_id', 'ID', WeekDays, 'NAME')

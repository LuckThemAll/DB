from db_connect import cur
from fields import *


class BaseModel(metaclass=ABCMeta):
    def __init__(self, table_name=None):
        self.table_name = table_name
        self.columns = {}

    def get_titles(self):
        return [self.columns[item].title for item in self.columns]

    def get_rows(self):

        pass


class NamedModel(BaseModel):
    def __init__(self, table_name=None, title=None):
        super().__init__(table_name)
        self.columns['id'] = IntegerField('ID', 'ID', 20)
        self.columns['name'] = StringField('NAME', title, 200)


class RefModel(BaseModel):
    def __init__(self, table_name):
        super().__init__(table_name)

    def get_titles(self):
        return [self.columns[item].source.columns['name'].title for item in self.columns]


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
        self.columns['order_number'] = IntegerField('ORDER_NUMBER', 'Порядок', 20)


class WeekDays(NamedModel):
    def __init__(self):
        super().__init__('WEEKDAYS', 'День недели')
        self.columns['order_number'] = IntegerField('ORDER_NUMBER', 'Порядок', 20)


class SubjectGroup(RefModel):
    def __init__(self):
        super().__init__('SUBJECT_GROUP')
        self.columns['subject_id'] = ReferenceField('ID', Subjects(), 'NAME')
        self.columns['group_id'] = ReferenceField('ID', Groups(), 'NAME')


class SubjectTeacher(RefModel):
    def __init__(self):
        super().__init__('SUBJECT_TEACHER')
        self.columns['subject_id'] = ReferenceField('ID', Subjects(), 'NAME')
        self.columns['teacher_id'] = ReferenceField('ID', Teachers(), 'NAME')


class SchedItems(RefModel):
    def __init__(self):
        super().__init__('SCHED_ITEM')
        self.columns['lesson_id'] = ReferenceField('ID', Lessons(), 'NAME')
        self.columns['subject_id'] = ReferenceField('ID', Subjects(), 'NAME')
        self.columns['audience_id'] = ReferenceField('ID', Audiences(), 'NAME')
        self.columns['group_id'] = ReferenceField('ID', Groups(), 'NAME')
        self.columns['teacher_id'] = ReferenceField('ID', Teachers(), 'NAME')
        self.columns['type_id'] = ReferenceField('ID', LessonTypes(), 'NAME')
        self.columns['weekday_id'] = ReferenceField('ID', WeekDays(), 'NAME')

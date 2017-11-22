from db_connect import cur
from sqlBuilred import *


class BaseModel(metaclass=ABCMeta):
    def __init__(self, table_name=None, title=None):
        self.table_name = table_name
        self.title = title
        self.columns = {}

    def get_titles(self):
        return [self.columns[item].title for item in self.columns]

    def get_rows(self, wheres=()):
        self.sql = SQLBuilder(self)
        self.sql.create_sql(wheres)
        print(self.sql.query)
        cur.execute(self.sql.query, (wheres[1], ))
        return cur.fetchall()


class NamedModel(BaseModel):
    def __init__(self, table_name=None, title=None):
        super().__init__(table_name, title)
        self.columns['id'] = IntegerField('ID', 'ID', 20)
        self.columns['name'] = StringField('NAME', title, 200)

    def get_col_names(self):
        return [self.table_name + '.' + self.columns[a].get_col_name() for a in self.columns]

    def get_tab_col(self, col_name):
        if col_name in self.columns.keys():
            return self.table_name + '.' + col_name


class RefModel(BaseModel):
    def __init__(self, table_name, title):
        super().__init__(table_name, title)

    def get_titles(self):
        return [self.columns[item].source.columns['name'].title for item in self.columns]

    def get_col_names(self):
        cols = self.__dict__['columns']
        return [cols[table].source.table_name + '.' + cols[table].field for table in cols]

    def get_tab_col(self, col_name):
        if col_name in self.columns.keys():
            return self.columns[col_name].source.table_name + '.' + self.columns[col_name].field


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
        super().__init__('SUBJECT_GROUP', 'Предметы')
        self.columns['subject_id'] = ReferenceField('ID', Subjects(), 'NAME')
        self.columns['group_id'] = ReferenceField('ID', Groups(), 'NAME')


class SubjectTeacher(RefModel):
    def __init__(self):
        super().__init__('SUBJECT_TEACHER', 'Нагрузка')
        self.columns['subject_id'] = ReferenceField('ID', Subjects(), 'NAME')
        self.columns['teacher_id'] = ReferenceField('ID', Teachers(), 'NAME')


class SchedItems(RefModel):
    def __init__(self):
        super().__init__('SCHED_ITEMS', 'Расписание')
        self.columns['lesson_id'] = ReferenceField('ID', Lessons(), 'NAME')
        self.columns['subject_id'] = ReferenceField('ID', Subjects(), 'NAME')
        self.columns['audience_id'] = ReferenceField('ID', Audiences(), 'NAME')
        self.columns['group_id'] = ReferenceField('ID', Groups(), 'NAME')
        self.columns['teacher_id'] = ReferenceField('ID', Teachers(), 'NAME')
        self.columns['type_id'] = ReferenceField('ID', LessonTypes(), 'NAME')
        self.columns['weekday_id'] = ReferenceField('ID', WeekDays(), 'NAME')

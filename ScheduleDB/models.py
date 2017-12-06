from db_connect import cur
from sqlBuilred import *


class BaseModel(metaclass=ABCMeta):
    def __init__(self, table_name=None, title=None):
        self.table_name = table_name
        self.title = title
        self.columns = {}
        self.sql_builder = SQLBuilder(self)

    def get_titles(self):
        return [self.columns[col].col_title for col in self.columns]

    @abstractmethod
    def fetch_all(self, sort_by_col):
        self.sql_builder.set_fields()
        self.sql_builder.set_from_table()
        self.sql_builder.add_sort_by_col(sort_by_col)
        self.sql_builder.where_col_names = []
        self.sql_builder.operators = []

    @abstractmethod
    def fetch_all_by_params(self, col_names, params, operators, sort_by_col):
        self.sql_builder.set_fields()
        self.sql_builder.set_from_table()
        self.sql_builder.add_where_col_names(col_names)
        self.sql_builder.add_operators(operators)
        self.sql_builder.add_sort_by_col(sort_by_col)


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

    def fetch_all(self, sort_by_col):
        BaseModel.fetch_all(self, sort_by_col)
        print(self.sql_builder.get_sql())
        cur.execute(self.sql_builder.get_sql())
        return cur.fetchall()

    def fetch_all_by_params(self, col_names, params, operators, sort_by_col):
        BaseModel.fetch_all_by_params(self, col_names, params, operators)
        print(self.sql_builder.get_sql())
        cur.execute(self.sql_builder.get_sql(), params)
        return cur.fetchall()


class RefModel(BaseModel):
    def __init__(self, table_name, title):
        super().__init__(table_name, title)

    def get_col_names(self):
        cols = self.__dict__['columns']
        return [cols[table].source.table_name + '.' + cols[table].field for table in cols]

    def get_tab_col(self, col_name):
        if col_name in self.columns.keys():
            return self.columns[col_name].source.table_name + '.' + self.columns[col_name].field

    def fetch_all(self, sort_by_col):
        BaseModel.fetch_all(self, sort_by_col)
        self.sql_builder.add_l_joins()
        print(self.sql_builder.get_sql())
        cur.execute(self.sql_builder.get_sql())
        return cur.fetchall()

    def fetch_all_by_params(self, col_names, params, operators, sort_by_col):
        BaseModel.fetch_all_by_params(self, col_names, params, operators)
        self.sql_builder.add_l_joins()
        print(self.sql_builder.get_sql())
        cur.execute(self.sql_builder.get_sql(), params)
        return cur.fetchall()


class Audiences(NamedModel):
    def __init__(self):
        super().__init__('AUDIENCES', 'Аудитории')


class Groups(NamedModel):
    def __init__(self):
        super().__init__('GROUPS', 'Группы')


class LessonTypes(NamedModel):
    def __init__(self):
        super().__init__('LESSON_TYPES', 'Вид занятий')


class Subjects(NamedModel):
    def __init__(self):
        super().__init__('SUBJECTS', 'Предметы')


class Teachers(NamedModel):
    def __init__(self):
        super().__init__('TEACHERS', 'Преподаватели')


class Lessons(NamedModel):
    def __init__(self):
        super().__init__('LESSONS', 'Порядок пар')
        self.columns['order_number'] = IntegerField('ORDER_NUMBER', 'Порядок', 20)


class WeekDays(NamedModel):
    def __init__(self):
        super().__init__('WEEKDAYS', 'Дни недели')
        self.columns['order_number'] = IntegerField('ORDER_NUMBER', 'Порядок', 20)


class SubjectGroup(RefModel):
    def __init__(self):
        super().__init__('SUBJECT_GROUP', 'Учебный план')
        self.columns['subject_id'] = ReferenceField('SUBJECT_ID', 'Предмет', 'ID', Subjects(), 'NAME')
        self.columns['group_id'] = ReferenceField('GROUP_ID', 'Группа', 'ID', Groups(), 'NAME')


class SubjectTeacher(RefModel):
    def __init__(self):
        super().__init__('SUBJECT_TEACHER', 'Нагрузка учителей')
        self.columns['subject_id'] = ReferenceField('SUBJECT_ID', 'Предмет', 'ID', Subjects(), 'NAME')
        self.columns['teacher_id'] = ReferenceField('TEACHER_ID', 'ФИО преподавателя', 'ID', Teachers(), 'NAME')


class SchedItems(RefModel):
    def __init__(self):
        super().__init__('SCHED_ITEMS', 'Расписание')
        self.columns['lesson_id'] = ReferenceField('LESSON_ID', 'Номер пары', 'ID', Lessons(), 'NAME')
        self.columns['subject_id'] = ReferenceField('SUBJECT_ID', 'Предмет', 'ID', Subjects(), 'NAME')
        self.columns['audience_id'] = ReferenceField('AUDIENCES_ID', 'Номер аудитории', 'ID', Audiences(), 'NAME')
        self.columns['group_id'] = ReferenceField('GROUP_ID', 'Группа', 'ID', Groups(), 'NAME')
        self.columns['teacher_id'] = ReferenceField('TEACHER_ID', 'ФИО преподавателя', 'ID', Teachers(), 'NAME')
        self.columns['type_id'] = ReferenceField('TYPE_ID', 'Тип пары', 'ID', LessonTypes(), 'NAME')
        self.columns['weekday_id'] = ReferenceField('WEEKDAY_ID', 'День недели', 'ID', WeekDays(), 'NAME')

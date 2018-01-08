from db_connect import cur
from sqlBuilder import *


class BaseModel(metaclass=ABCMeta):
    class Columns:
        def get_col(self, col_name):
            return getattr(self, col_name)

        def get_titles(self):
            return [self.get_col(col).col_title for col in self.__dict__]

        def get_titles_without_id(self):
            return [self.get_col(col).col_title for col in self.__dict__ if col != 'id']

        def get_cols_without_id(self):
            return [col for col in self.__dict__ if col != 'id']

        def get_col_names(self, table_name):
            return [self.get_col(col).get_col_name(table_name) for col in self.__dict__]

    def __init__(self, table_name, title):
        self.table_name = table_name
        self.title = title
        self.columns = self.Columns()
        self.sql_builder = SQLBuilder(self)

    def build_base_sql(self, sort_by_col):
        self.sql_builder.clear_fields()
        self.sql_builder.set_fields()
        self.sql_builder.set_from_table()
        self.sql_builder.add_sort_by_col(sort_by_col)

    @abstractmethod
    def fetch_all(self, sort_by_col):
        self.build_base_sql(sort_by_col)

    @abstractmethod
    def fetch_all_by_params(self, col_names, params, operators, logic_operator, sort_by_col):
        self.build_base_sql(sort_by_col)
        self.sql_builder.add_where_col_names(col_names)
        self.sql_builder.add_operators(operators)
        self.sql_builder.add_logic_operator(logic_operator)


class NamedModel(BaseModel):
    def __init__(self, table_name, title):
        super().__init__(table_name, title)
        self.columns.id = IntegerField('ID', 'ID')
        self.columns.name = StringField('NAME', title)

    def get_tab_col(self, col_name):
        return getattr(self.columns, col_name).get_col_name(self.table_name)

    def get_tab_col_for_sort(self, col_name):
        if col_name == 'name' and 'order_number' in self.columns.__dict__:
            return getattr(self.columns, 'order_number').get_col_name(self.table_name)
        return getattr(self.columns, col_name).get_col_name(self.table_name)

    def fetch_all(self, sort_by_col):
        BaseModel.fetch_all(self, sort_by_col)
        print(self.sql_builder.get_sql())
        cur.execute(self.sql_builder.get_sql())
        return cur.fetchall()

    def fetch_all_by_params(self, col_names, params, operators, logic_operator, sort_by_col):
        BaseModel.fetch_all_by_params(self, col_names, params, operators, logic_operator, sort_by_col)
        print(self.sql_builder.get_sql())
        cur.execute(self.sql_builder.get_sql(), params)
        return cur.fetchall()


class RefModel(BaseModel):
    def __init__(self, table_name, title):
        super().__init__(table_name, title)
        self.type = 'refs'
        self.columns.id = IntegerField('ID', 'ID')

    def get_tab_col(self, col):
        return self.columns.get_col(col).get_col_name(self.table_name)

    def get_tab_col_for_sort(self, col):
        if isinstance(self.columns.get_col(col), ReferenceField) and \
                        'order_number' in self.columns.get_col(col).source.columns.__dict__:
            return self.columns.get_col(col).source.get_tab_col('order_number')
        return self.columns.get_col(col).get_col_name(self.table_name)

    def fetch_all(self, sort_by_col='id'):
        BaseModel.fetch_all(self, sort_by_col)
        self.sql_builder.add_l_joins()
        print(self.sql_builder.get_sql())
        cur.execute(self.sql_builder.get_sql())
        return cur.fetchall()

    def fetch_all_by_params(self, col_names, params, operators, logic_operator, sort_by_col):
        BaseModel.fetch_all_by_params(self, col_names, params, operators, logic_operator, sort_by_col)
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
        super().__init__('LESSONS', 'Пары')
        self.columns.order_number = IntegerField('ORDER_NUMBER', 'Номер пары')


class WeekDays(NamedModel):
    def __init__(self):
        super().__init__('WEEKDAYS', 'Дни недели')
        self.columns.order_number = IntegerField('ORDER_NUMBER', 'Порядок')


class SubjectGroup(RefModel):
    def __init__(self):
        super().__init__('SUBJECT_GROUP', 'Учебный план')
        self.columns.subject_id = ReferenceField('SUBJECT_ID', 'Предмет', 'ID', Subjects(), 'NAME')
        self.columns.group_id = ReferenceField('GROUP_ID', 'Группа', 'ID', Groups(), 'NAME')


class SubjectTeacher(RefModel):
    def __init__(self):
        super().__init__('SUBJECT_TEACHER', 'Нагрузка учителей')
        self.columns.subject_id = ReferenceField('SUBJECT_ID', 'Предмет', 'ID', Subjects(), 'NAME')
        self.columns.teacher_id = ReferenceField('TEACHER_ID', 'ФИО преподавателя', 'ID', Teachers(), 'NAME')


class SchedItems(RefModel):
    def __init__(self):
        super().__init__('SCHED_ITEMS', 'Расписание')
        self.columns.lesson_id = ReferenceField('LESSON_ID', 'Номер пары', 'ID', Lessons(), 'NAME')
        self.columns.subject_id = ReferenceField('SUBJECT_ID', 'Предмет', 'ID', Subjects(), 'NAME')
        self.columns.audience_id = ReferenceField('AUDIENCE_ID', 'Номер аудитории', 'ID', Audiences(), 'NAME')
        self.columns.group_id = ReferenceField('GROUP_ID', 'Группа', 'ID', Groups(), 'NAME')
        self.columns.teacher_id = ReferenceField('TEACHER_ID', 'ФИО преподавателя', 'ID', Teachers(), 'NAME')
        self.columns.type_id = ReferenceField('TYPE_ID', 'Тип пары', 'ID', LessonTypes(), 'NAME')
        self.columns.weekday_id = ReferenceField('WEEKDAY_ID', 'День недели', 'ID', WeekDays(), 'NAME')

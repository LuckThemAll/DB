from db_connect import *
from sqlBuilder import *


class BaseModel(metaclass=ABCMeta):
    class Columns:
        def get_col(self, col_name):
            return getattr(self, col_name.lower())

        def get_titles(self):
            return [self.get_col(col).col_title for col in self.__dict__]

        def get_titles_without_id(self):
            return [self.get_col(col).col_title for col in self.__dict__ if col != 'id']

        def get_cols_without_id(self):
            return [col for col in self.__dict__ if col != 'id']

        def get_col_names(self, table_name):
            return [self.get_col(col).get_col_name(table_name) for col in self.__dict__]

        def get_keys(self):
            return self.__dict__.keys()

    def __init__(self, table_name, title):
        self.table_name = table_name
        self.title = title
        self.columns = self.Columns()
        self.sql_builder = SQLBuilder(self)

    def build_base_sql(self, sort_by_col='id', sort_type='inc'):
        self.sql_builder.clear_fields()
        self.sql_builder.set_fields()
        self.sql_builder.set_from_table()
        self.sql_builder.add_sort_by_col(sort_by_col)
        self.sql_builder.add_sort_type(sort_type)

    @abstractmethod
    def fetch_all(self, *fields):
        self.sql_builder.clear_fields()
        if fields.__len__() > 0:
            fields = [field for field in fields]
            self.sql_builder.set_fields(fields, name=False)
        else:
            self.sql_builder.set_fields(self.columns.get_cols_without_id(), name=False)
        self.sql_builder.set_from_table()

    @abstractmethod
    def fetch_one(self, id):
        self.sql_builder.clear_fields()
        self.sql_builder.set_fields(self.columns.get_cols_without_id(), name=False)
        self.sql_builder.set_from_table()

    @abstractmethod
    def fetch_all_names(self, sort_by_col, sort_type):
        self.build_base_sql(sort_by_col, sort_type)

    @abstractmethod
    def fetch_all_by_params(self, col_names, params, operators, logic_operator, sort_by_col, sort_type):
        self.build_base_sql(sort_by_col)
        self.sql_builder.add_where_col_names(col_names)
        self.sql_builder.add_operators(operators)
        self.sql_builder.add_logic_operator(logic_operator)
        self.sql_builder.add_sort_type(sort_type)


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

    def fetch_all_names(self, sort_by_col='id', sort_type='inc'):
        BaseModel.fetch_all_names(self, sort_by_col, sort_type)
        print(self.sql_builder.get_sql())
        cur.execute(self.sql_builder.get_sql())
        return cur.fetchall()

    def fetch_all_by_params(self, col_names, params, operators, logic_operator, sort_by_col, sort_type):
        BaseModel.fetch_all_by_params(self, col_names, params, operators, logic_operator, sort_by_col, sort_type)
        print(self.sql_builder.get_sql())
        cur.execute(self.sql_builder.get_sql(), params)
        return cur.fetchall()

    def fetch_all(self, *fields):
        BaseModel.fetch_all(self, *fields)
        print(self.sql_builder.get_sql())
        cur.execute(self.sql_builder.get_sql())
        return cur.fetchall()

    def fetch_one(self, id):
        BaseModel.fetch_all(self)
        self.sql_builder.add_where_col_names('id')
        self.sql_builder.add_operators('=')
        cur.execute(self.sql_builder.get_sql(), get_list(id))
        return cur.fetchone()


class RefModel(BaseModel):
    def __init__(self, table_name, title):
        super().__init__(table_name, title)
        self.columns.id = IntegerField('ID', 'ID')

    def get_tab_col(self, col):
        return self.columns.get_col(col).get_col_name(self.table_name)

    def get_tab_col_for_sort(self, col):
        print(self.columns.__dict__)
        if isinstance(self.columns.get_col(col), ReferenceField) and \
                        'order_number' in self.columns.get_col(col).source.columns.__dict__:
            return self.columns.get_col(col).source.get_tab_col('order_number')
        return self.columns.get_col(col).get_col_name(self.table_name)

    def fetch_all_names(self, sort_by_col='id', sort_type='inc'):
        BaseModel.fetch_all_names(self, sort_by_col, sort_type)
        self.sql_builder.add_l_joins()
        print(self.sql_builder.get_sql())
        cur.execute(self.sql_builder.get_sql())
        return cur.fetchall()

    def fetch_all_by_params(self, col_names, params, operators, logic_operator, sort_by_col, sort_type):
        BaseModel.fetch_all_by_params(self, col_names, params, operators, logic_operator, sort_by_col, sort_type)
        self.sql_builder.add_l_joins()
        print(self.sql_builder.get_sql())
        cur.execute(self.sql_builder.get_sql(), params)
        return cur.fetchall()

    def fetch_all(self, *fields):
        BaseModel.fetch_all(self, *fields)
        cur.execute(self.sql_builder.get_sql())
        print(self.sql_builder.get_sql())
        return cur.fetchall()

    def fetch_one(self, id):
        BaseModel.fetch_all(self)
        self.sql_builder.add_where_col_names('id')
        self.sql_builder.add_operators('=')
        cur.execute(self.sql_builder.get_sql(), get_list(id))
        return cur.fetchone()


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
        self.columns.audience_id = ReferenceField('AUDIENCE_ID', 'Аудитория', 'ID', Audiences(), 'NAME')
        self.columns.group_id = ReferenceField('GROUP_ID', 'Группа', 'ID', Groups(), 'NAME')
        self.columns.teacher_id = ReferenceField('TEACHER_ID', 'Преподователь', 'ID', Teachers(), 'NAME')
        self.columns.type_id = ReferenceField('TYPE_ID', 'Тип пары', 'ID', LessonTypes(), 'NAME')
        self.columns.weekday_id = ReferenceField('WEEKDAY_ID', 'День недели', 'ID', WeekDays(), 'NAME')


tables = (
          Audiences(),
          Groups(),
          Lessons(),
          LessonTypes(),
          SchedItems(),
          Subjects(),
          SubjectGroup(),
          SubjectTeacher(),
          Teachers(),
          WeekDays()
        )
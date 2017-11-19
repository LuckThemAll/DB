from db_connect import cur
from fields import *


class BaseModel(metaclass=ABCMeta):
    def __init__(self, table_name=None, title=None):
        self.table_name = table_name
        self.title = title
        self.columns = {}

    def get_titles(self):
        return [self.columns[item].title for item in self.columns]


class NamedModel(BaseModel):
    def __init__(self, table_name=None, title=None):
        super().__init__(table_name, title)
        self.columns['id'] = IntegerField('ID', 'ID', 20)
        self.columns['name'] = StringField('NAME', title, 200)

    def get_rows(self):
        def get_col_names():
            return [self.columns[a].get_col_name() for a in self.columns]

        col_names = get_col_names()
        query = 'select '
        for i, col_name in enumerate(col_names):
            if i == 0:
                query += col_name
            else:
                query += ', ' + col_name
        query += ' from ' + self.table_name
        cur.execute(query)
        return cur.fetchall()


class RefModel(BaseModel):
    def __init__(self, table_name, title):
        super().__init__(table_name, title)

    def get_titles(self):
        return [self.columns[item].source.columns['name'].title for item in self.columns]

    def get_rows(self):
        query = 'select '

        def get_col_names():
            result = []
            for table in self.__dict__['columns']:
                result.append('{0}.{1}'.format(self.__dict__['columns'][table].source.table_name,
                                               self.__dict__['columns'][table].field)
                              )
            return result

        for i, col_name in enumerate(get_col_names()):
            if i == 0:
                query += col_name
            else:
                query += ', ' + col_name
        query += ' from ' + self.table_name + ' '

        def l_joins():
            result = []
            for table in self.__dict__['columns']:
                result.append('left join {0} on {0}.{1}={2}.{3} '.
                              format(self.__dict__['columns'][table].source.table_name,
                                     self.__dict__['columns'][table].ref,
                                     self.table_name,
                                     table)
                              )
            return result
        for j in l_joins():
            query += j
        print(query)
        cur.execute(query)
        return cur.fetchall()


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

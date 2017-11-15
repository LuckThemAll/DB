from db_connect import cur
from abc import *


class NamedModel(metaclass=ABCMeta):
    def __init__(self, title='String', table_name='String', pixels=50):
        self.id = {'col_name': 'ID', 'title': 'Ключ', 'pixels': 20}
        self.name = {'col_name': 'NAME', 'title': title, 'pixels': pixels}
        self.table_name = table_name

    def get_names(self):
        sql = 'select %s from %s' % (self.name['col_name'], self.table_name)
        if cur.execute(sql):
            return [col[0] for col in cur.fetchall()]

    def get_ids(self):
        sql = 'select %s from %s' % (self.id['col_name'], self.table_name)
        if cur.execute(sql):
            return [col[0] for col in cur.fetchall()]

    def find_one(self, id):
        sql = 'select NAME from %s s where s.ID=%d' % (self.table_name, id)
        if cur.execute(sql):
            return cur.fetchall()[0][0]

    def get_name_title(self):
        return self.name['title']


class Audiences(NamedModel):
    def __init__(self):
        super().__init__('Номер аудитории', 'AUDIENCES')

    def get_titles(self):
        return [self.id['title'], self.name['title']]

    def get_rows(self):
        sql = 'select %s.ID, %s.NAME from %s' % (self.table_name, self.table_name, self.table_name)
        if cur.execute(sql):
            return cur.fetchall()


class Groups(NamedModel):
    def __init__(self):
        super().__init__('Группа', 'GROUPS')

    def get_titles(self):
        return [self.id['title'], self.name['title']]

    def get_rows(self):
        sql = 'select %s.ID, %s.NAME from %s' % (self.table_name, self.table_name, self.table_name)
        if cur.execute(sql):
            return cur.fetchall()


class Lessons(NamedModel):
    def __init__(self):
        super().__init__('Пара', 'LESSONS')
        self.order_number = {'col_name': 'ORDER_NUMBER', 'title': 'Порядок', 'pixels': 20}

    def get_titles(self):
        return [self.id['title'], self.name['title'], self.order_number['title']]

    def get_rows(self):
        sql = 'select %s.ID, %s.NAME, %s.ORDER_NUMBER from %s' % (self.table_name, self.table_name, self.table_name, self.table_name)
        if cur.execute(sql):
            return cur.fetchall()


class LessonTypes(NamedModel):
    def __init__(self):
        super().__init__('Тип занятия', 'LESSON_TYPES', 50)

    def get_titles(self):
        return [self.id['title'], self.name['title']]

    def get_rows(self):
        sql = 'select %s.ID, %s.NAME from %s' % (self.table_name, self.table_name, self.table_name)
        if cur.execute(sql):
            return cur.fetchall()


class Subjects(NamedModel):
    def __init__(self):
        super().__init__('Предмет', 'SUBJECTS')

    def get_titles(self):
        return [self.id['title'], self.name['title']]

    def get_rows(self):
        sql = 'select %s.ID, %s.NAME from %s' % (self.table_name, self.table_name, self.table_name)
        if cur.execute(sql):
            return cur.fetchall()


class Teachers(NamedModel):
    def __init__(self):
        super().__init__('ФИО', 'TEACHERS')

    def get_titles(self):
        return [self.id['title'], self.name['title']]

    def get_rows(self):
        sql = 'select %s.ID, %s.NAME from %s' % (self.table_name, self.table_name, self.table_name)
        if cur.execute(sql):
            return cur.fetchall()


class Select:
    def __init__(self, table_name, magic):
        self.joins = ''
        self.cols = ''
        size = len(magic)-1
        for i, item in enumerate(magic):
            self.cols += magic[item]['External_Table'] + '.NAME'
            if i != size:
                self.cols += ','
            self.cols += ' '
            self.add_join(magic[item]['External_Table'],
                          table_name,
                          magic[item]['External_Ref'],
                          item)
        self.sql = 'select ' + self.cols + ' from ' + table_name + self.joins

    def __call__(self):
        return self.sql

    def add_join(self, ext_table_name, int_table_name, ext_param, int_param):
        params = ' on %s.%s=%s.%s ' % (ext_table_name, ext_param, int_table_name, int_param)
        self.joins += ' left join ' + ext_table_name + params


class SubjectGroup:
    def __init__(self):
        self.group_id = {'External_Table': Groups().table_name,
                         'title': 'Группа',
                         'External_Ref': Groups().id['col_name']
                         }
        self.subject_id = {'External_Table': Subjects().table_name,
                           'title': 'Предмет',
                           'External_Ref': Subjects().id['col_name']
                           }

    def get_titles(self):
        return [self.group_id['title'], self.subject_id['title']]

    def get_rows(self):
        sql = Select('SUBJECT_GROUP', self.__dict__)()
        cur.execute(sql)
        return cur.fetchall()


class SubjectTeacher:
    def __init__(self):
        self.teacher_id = {'External_Table': Teachers().table_name,
                           'title': 'ФИО',
                           'External_Ref': Teachers().id['col_name']
                           }
        self.subject_id = {'External_Table': Subjects().table_name,
                           'title': 'Предмет',
                           'External_Ref': Subjects().id['col_name']
                           }

    def get_titles(self):
        return [self.teacher_id['title'], self.subject_id['title']]

    def get_rows(self):
        sql = Select('SUBJECT_TEACHER', self.__dict__)()
        print(sql)
        cur.execute(sql)
        return cur.fetchall()


class WeekDays(NamedModel):
    def __init__(self):
        super().__init__('День недели', 'WEEKDAYS', 100)
        self.order_number = {'col_name': 'ORDER_NUMBER', 'title': 'Порядок', 'pixels': 20}

    def get_titles(self):
        return [self.id['title'], self.name['title'], self.order_number['title']]

    def get_rows(self):
        sql = 'select %s.ID, %s.NAME, %s.%s from %s' % (self.table_name, self.table_name, self.table_name, self.order_number['col_name'], self.table_name)
        if cur.execute(sql):
            return cur.fetchall()


class SchedItems:
    def __init__(self):
        self.lesson_id = {'External_Table': Lessons().table_name,
                          'title': 'Номер пары',
                          'External_Ref': Lessons().id['col_name'],
                          }

        self.subject_id = {'External_Table': Subjects().table_name,
                           'title': 'Предмет',
                           'External_Ref': Subjects().id['col_name']
                           }

        self.audience_id = {'External_Table': Audiences().table_name,
                            'title': 'Номер кабинета',
                            'External_Ref': Audiences().id['col_name']
                            }

        self.group_id = {'External_Table': Groups().table_name,
                         'title': 'Группа',
                         'External_Ref': Groups().id['col_name']
                         }

        self.teacher_id = {'External_Table': Teachers().table_name,
                           'title': 'ФИО',
                           'External_Ref': Teachers().id['col_name']
                           }

        self.type_id = {'External_Table': LessonTypes().table_name,
                        'title': 'Вид занятия',
                        'External_Ref': LessonTypes().id['col_name']
                        }

        self.weekday_id = {'External_Table': WeekDays().table_name,
                           'title': 'День недели',
                           'External_Ref': WeekDays().id['col_name']
                           }

    def get_titles(self):
        return [self.lesson_id['title'],
                self.subject_id['title'],
                self.audience_id['title'],
                self.group_id['title'],
                self.teacher_id['title'],
                self.type_id['title'],
                self.weekday_id['title']]

    def get_rows(self):
        sql = Select('SCHED_ITEMS', self.__dict__)()
        cur.execute(sql)
        return cur.fetchall()

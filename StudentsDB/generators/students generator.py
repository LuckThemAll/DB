import random

f_out = open('out.txt', 'w')


def gen_birthdate():
    day = random.randint(1, 29)
    month = random.randint(1, 12)
    year = random.randint(1980, 2000)
    return '%d-%d-%d' % (year, month, day)


names = ['Artem', 'Vladimir', 'Ivan', 'Masha', 'Olga']
surnames = ['Guk', 'Smith', 'Vasilenko', 'North', 'Mitler']
fatherNames = ['Olegovich', 'Dmitrievich', 'Vladimirovich', 'Alexeevich']

f_out.write("""CREATE DATABASE '../students.fdb'

CREATE TABLE students(
    id INTEGER,
    name VARCHAR(100),
    birthday DATE,
    group_id INTEGER
);

""")

id = 1
group_id = 1

for name in names:
    for surname in surnames:
        for fatherName in fatherNames:
            fio = '%s %s %s' % (surname, name, fatherName)
            birth_date = str(gen_birthdate())
            sql_comm = "INSERT INTO students VALUES ('" + str(id) + "', '" + fio + "', '" + birth_date + "', '" + str(group_id) + "');\n"
            f_out.write(sql_comm)
            id += 1
            group_id = group_id + 1 if group_id < 5 else 1



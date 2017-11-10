import random

f_out = open('out.txt', 'w')

f_out.write("""CONNECT '.../students.fdb'

CREATE TABLE marks(
    id INTEGER,
    student_id INTEGER,
    subject_id INTEGER,
    mark INTEGER
);

""")

subject_id = 1
id = 1
for student_id in range(1, 101):
    for c in range(0, 30, 5):
        f_out.write("INSERT INTO marks VALUES(%d, %d, %d, %d);\n" % (id, student_id, subject_id + c, random.randint(1, 10)))
        id += 1
    subject_id = subject_id + 1 if subject_id < 5 else 1

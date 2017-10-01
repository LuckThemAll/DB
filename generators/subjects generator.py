f_out = open('out.txt', 'w')
f_in = open('in.txt', 'r')

subjects = []
for line in f_in:
    subjects.append(line.strip())

f_out.write("""CONNECT '../students.fdb'

CREATE TABLE subjects(
    id INTEGER,
    name VARCHAR(30),
    group_id INTEGER
);

""")

group_id = 1

for id, subject in enumerate(subjects):
    f_out.write("INSERT INTO subjects VALUES(%d, %s, %d);\n" % (id + 1, subject, group_id))
    group_id = group_id + 1 if group_id < 5 else 1

f_out = open('out.txt', 'w')

groups = ['B8102', 'B8103', 'B8203a', 'C8434', 'E5604']

f_out.write("""CONNECT '../students.fdb'

CREATE TABLE groups(
    id INTEGER,
    name VARCHAR(10)
);

""")

for id, group in enumerate(groups):
    f_out.write("INSERT INTO groups VALUES(%d, '%s');\n" % (id + 1, group))

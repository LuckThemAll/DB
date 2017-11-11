from flask import Flask
from flask import request
import fdb

app = Flask(__name__)

@app.route('/', )

def get_students():

    con = fdb.connect(
        dsn='localhost:C:/Users/Artem/Downloads/TIMETABLE.FDB',
        user='SYSDBA',
        password='masterkey',
        charset='UTF8'
    )

    try:
        cur = con.cursor()


        cur.execute(''' select RDB$RELATION_NAME from RDB$RELATIONS
                        where (RDB$SYSTEM_FLAG = 0) AND (RDB$RELATION_TYPE = 0)
                        order by RDB$RELATION_NAME''')
        out_put = '''   <form name="from_name">
                            <select name="search">
                        '''
        for row in cur.fetchall():
            str_name = str(row[0]).strip()
            out_put += '<option>' + str_name + '</option>'
        out_put += '</select><input type="submit"></input></from><br>'
        get_stud = request.args.get('search', '')
        sql = 'select * from %s ' % get_stud
        cur.execute(sql)
        for row in cur.fetchall():
            out_put += str(row) + '<br>'
        return out_put
    finally:
        con.close()
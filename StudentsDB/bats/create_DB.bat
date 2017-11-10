SET isql=C:\"Program Files"\Firebird\Firebird_3_0\isql.exe -u SYSDBA -p masterkey
SET sqlfolder=C:\Users\Artem\Desktop\DB\Sql

%isql% -i %sqlfolder%\students.sql
%isql% -i %sqlfolder%\groups.sql
%isql% -i %sqlfolder%\subjects.sql
%isql% -i %sqlfolder%\marks.sql

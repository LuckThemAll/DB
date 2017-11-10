SET isql=C:\"Program Files"\Firebird\Firebird_2_5\bin\isql.exe -u SYSDBA -p masterkey
SET sqlfolder=C:\Users\Artem\Desktop\DB\Sql

del C:\Users\Artem\Desktop\DB\STUDENTS.FDB

%isql% -i %sqlfolder%\students.sql
%isql% -i %sqlfolder%\groups.sql
%isql% -i %sqlfolder%\subjects.sql
%isql% -i %sqlfolder%\marks.sql
pause
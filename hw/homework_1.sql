/* ��� ������ ������ ������ �������, � ������� ���� �� ��������� */

select g.name, (select list(distinct extract(month from s.BIRTHDAY))
                from STUDENTS s
                where s.GROUP_ID = g.ID
                )
 from GROUPS g;

/* ��������, ��������������� �� �������� �������� ����� */

select 
    s.NAME, 
    avg(cast(m.mark as float)) as mid_score 
from STUDENTS s 
inner join MARKS m on m.STUDENT_ID = s.ID 
group by s.NAME
order by mid_score desc

/* ��������, ��������������� �� �������� ������������ */

select 
    s.NAME, 
    avg(cast(m.mark as float)) as mid_score 
from SUBJECTS s 
inner join MARKS m on m.SUBJECT_ID = s.ID
group by s.NAME
order by mid_score desc

/* */

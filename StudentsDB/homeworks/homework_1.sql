/*	3 запрос (дл€ каждого студента предметы с оценкой ниже средней дл€ данного студента)	*/

select  s.NAME, list(sbjts) 
from STUDENTS s 
inner join  (
                select sj.name as sbjts, s.NAME as s_name
                from STUDENTS s
                inner join MARKS m on m.STUDENT_ID = s.ID
                inner join SUBJECTS sj on m.SUBJECT_ID = sj.ID 
                inner join (
                                select  s.id as s_id, 
                                avg(m.mark) as savg 
                                from STUDENTS s 
                                inner join MARKS m on m.STUDENT_ID = s.ID 
                                group by s.id
                            ) on s.id = s_id 
                group by s.NAME, sj.NAME, savg 
                having avg(m.mark) < savg
            ) on s.NAME = s_name
group by s.NAME

-------------------------------------------------------------------------------------------------

/*	1 запрос (мес€цы рождени€ наиболее активных прогульщиков (не имеющих оценок по наибольшему количеству предметов))	*/

select
    list(distinct bmonth),
    skipped
from    (
            select  extract(month from s.BIRTHDAY) as bmonth,
                    count(*) as skipped
            from STUDENTS s
            inner join GROUPS g on g.ID = s.GROUP_ID
            inner join SUBJECTS sj on sj.GROUP_ID = g.ID
            left join MARKS m on m.SUBJECT_ID = sj.ID and m.STUDENT_ID = s.ID
            where m.id is NUll
            group by s.NAME, s.ID, bmonth
        )
group by skipped
order by skipped desc

-------------------------------------------------------------------------------------------------
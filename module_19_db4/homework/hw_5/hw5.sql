-- общее количество учеников
select count(*) as students_cnt from students;

-- средняя оценка
select avg(grade) as avg_grade from assignments_grades;

-- количество учеников, которые не сдали работы
select count(*) from students
where students.student_id not in (select assignments_grades.student_id from assignments_grades)

-- количество учеников, которые просрочили дедлайн
select count(distinct(student_id)) from
                    (select * from assignments_grades
                    join main.assignments a on a.assisgnment_id = assignments_grades.assisgnment_id
                    where date > a.due_date
                    group by student_id);

-- количество повторных попыток сдать работу
select sum(cnt) from (
    select *, count(1) as cnt from assignments_grades
    join main.assignments a on a.assisgnment_id = assignments_grades.assisgnment_id
    where date > a.due_date
    group by student_id
    having cnt > 1);
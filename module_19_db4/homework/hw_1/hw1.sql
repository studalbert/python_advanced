select avg(grade) as avg_grade, a.teacher_id, t.full_name  from assignments_grades
inner join assignments a on assignments_grades.assisgnment_id = a.assisgnment_id
inner join teachers t on a.teacher_id = t.teacher_id
group by a.teacher_id
order by avg_grade
limit 1;
select s.full_name,assignments_grades.student_id, avg(assignments_grades.grade) as avg_grade from assignments_grades
inner join students s on s.student_id = assignments_grades.student_id
group by assignments_grades.student_id
order by avg_grade desc
limit 10;
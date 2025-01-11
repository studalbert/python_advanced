select students.full_name, group_id from students
inner join
    (select group_id as gr_id, t_id from students_groups
     inner join
        (select avg(assignments_grades.grade) as avg_grade, teacher_id t_id from assignments_grades
        inner join assignments a on a.assisgnment_id = assignments_grades.assisgnment_id
        group by t_id
        order by avg_grade desc
        limit 1) on t_id = teacher_id) on group_id = gr_id;
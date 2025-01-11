select avg(grade) from assignments_grades
where assisgnment_id in (
    select assisgnment_id from assignments
                          where assignment_text
                          like 'прочитать%' or assignment_text like 'выучить%'
    );
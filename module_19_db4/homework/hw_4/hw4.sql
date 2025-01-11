select avg(cnt), min(cnt), max(cnt)
from (select s.group_id, count(*) as cnt from assignments_grades
      join students s on assignments_grades.student_id = s.student_id
      join assignments a on assignments_grades.assisgnment_id = a.assisgnment_id
      where assignments_grades.date > a.due_date
      group by s.group_id);
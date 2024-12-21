select Outcomes.battle
from Outcomes
join Ships
    on Outcomes.ship = Ships.name
where Ships.class = 'Kongo'
select name from ships
join classes on classes.class = ships.class
where name = classes.class

union

select ship from outcomes
join classes on classes.class = outcomes.ship
where ship = classes.class
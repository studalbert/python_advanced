select maker, Laptop.speed
from Product
join Laptop
on Product.model = Laptop.model
where hd >= 10
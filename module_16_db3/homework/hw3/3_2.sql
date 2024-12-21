select Product.model, PC.price
from Product
join PC
on Product.model = PC.model
where Product.maker = 'B'
union all
select Product.model, Laptop.price
from Product
join Laptop
on Product.model = Laptop.model
where Product.maker = 'B'
union all
select Product.model, Printer.price
from Product
join Printer
on Product.model = Printer.model
where Product.maker = 'B'

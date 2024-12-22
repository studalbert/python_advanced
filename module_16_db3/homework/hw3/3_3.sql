Select distinct(maker) from Product
inner join PC
on Product.model = PC.model
where speed >= 450

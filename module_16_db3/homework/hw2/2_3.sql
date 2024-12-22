select "order".order_no, manager.full_name, customer.full_name
from "order"
left join manager
on "order".manager_id = manager.manager_id
left join customer
on "order".customer_id = customer.customer_id
where manager.city != customer.city;
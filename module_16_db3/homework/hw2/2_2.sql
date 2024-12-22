-- select "customer".full_name
-- from customer
-- where customer.customer_id not in
--       (select distinct("order".customer_id) from "order");

select "customer".full_name
from customer
left join "order"
on customer.customer_id = order.customer_id
where "order".customer_id IS NULL;
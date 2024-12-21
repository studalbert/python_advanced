select "order".order_no, customer.full_name
from "order"
left join customer
on "order".customer_id = customer.customer_id
where "order".manager_id is null;
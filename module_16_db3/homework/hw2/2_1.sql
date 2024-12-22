select customer.full_name, manager.full_name, "order".purchase_amount, "order".date
from "order"
left join customer
on "order".customer_id = customer.customer_id
left join manager
on "order".manager_id = manager.manager_id;

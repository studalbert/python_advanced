SELECT t1.full_name customer1, t2.full_name customer2
FROM customer t1
JOIN customer t2
ON t1.city = t2.city AND t1.manager_id = t2.manager_id
WHERE t1.customer_id < t2.customer_id;
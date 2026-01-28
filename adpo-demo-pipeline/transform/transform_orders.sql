SELECT
  o.order_id,
  o.customer_id,
  SUM(i.price) AS total_amount
FROM orders_raw o
JOIN order_items i ON o.order_id = i.order_id
GROUP BY 1,2;

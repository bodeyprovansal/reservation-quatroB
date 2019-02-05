-- Fetches the most popular categories
SELECT `name`, (SELECT COUNT(*) FROM `warehouse`.`fact` WHERE category_id=c.category_id) as count FROM `warehouse`.`categories` c;

-- Fetches the most popular time of day for a reservation
SELECT hour, count(hour) AS count FROM `warehouse`.`time` GROUP BY hour;

-- Fetches the most popular day of the week for a reservation
SELECT dayofweek, count(dayofweek) AS count FROM `warehouse`.`time` GROUP BY dayofweek;

-- Customers with the most orders
SELECT
  c.customer_id,
  c.first_name,
  c.last_name,
  c.phone_number,
  c.email_address,
  COUNT(c.customer_id) as count
FROM `warehouse`.`customers` c
INNER JOIN `warehouse`.`fact` f on f.customer_id = c.customer_id
INNER JOIN `warehouse`.`orders` o on o.order_id = f.order_id
GROUP BY c.customer_id
ORDER BY COUNT(c.customer_id) DESC;

-- Customers that canceled their reservation (view)
CREATE VIEW canceled AS (
  SELECT
    f.order_id,
    f.customer_id,
    o.detailed_description,
    ca.name,
    c.first_name,
    c.last_name,
    c.phone_number,
    c.email_address
  FROM `warehouse`.`orders` o
  INNER JOIN `warehouse`.`fact` f on f.order_id = o.order_id
  INNER JOIN `warehouse`.`categories` ca on ca.category_id = f.category_id
  INNER JOIN `warehouse`.`customers` c on c.customer_id = f.customer_id
  RIGHT JOIN `warehouse`.`reservations` r on r.reservation_id = f.reservation_id
  WHERE r.reservation_id IS NOT NULL
);

SELECT * FROM canceled;

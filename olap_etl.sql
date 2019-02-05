INSERT INTO `warehouse`.`categories`
SELECT category_id, name from `cr`.`categories`;

INSERT INTO `warehouse`.`customers`
SELECT customer_id, first_name, last_name, phone_number, email_address from `cr`.`customers`;

INSERT INTO `warehouse`.`orders`
SELECT order_id, detailed_description from `cr`.`orders`;

INSERT INTO `warehouse`.`reservations`
SELECT reservation_id, reservation_key from `cr`.`reservations`;

INSERT INTO `warehouse`.`time`
SELECT order_id, YEAR(order_date), MONTH(order_date), DAYOFWEEK(order_date), HOUR(order_time) from `cr`.`orders`;

INSERT INTO `warehouse`.`fact`
SELECT o.order_id, o.customer_id, reservation_id, category_id, o.order_id as time_id from `cr`.`orders` o
RIGHT JOIN `cr`.`reservations` r on r.customer_id = o.customer_id;

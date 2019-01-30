DROP DATABASE IF EXISTS cr;
CREATE SCHEMA cr;
use cr;

CREATE TABLE customers (
  customer_id INT PRIMARY KEY AUTO_INCREMENT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  phone_number VARCHAR(50) NOT NULL,
  email_address VARCHAR(50) NOT NULL
);

CREATE TABLE categories (
  category_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL
);

CREATE TABLE orders (
  order_id INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT NOT NULL,
  category_id INT NOT NULL,
  detailed_description VARCHAR(100) NOT NULL,
  order_date DATE NOT NULL,
  order_time TIME NOT NULL,

  CONSTRAINT orders_fk_categories
    FOREIGN KEY (category_id)
    REFERENCES categories (category_id),
  CONSTRAINT orders_fk_customers
    FOREIGN KEY (customer_id)
    REFERENCES customers (customer_id)
);

CREATE TABLE reservations (
  reservation_id INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT NOT NULL,
  order_id INT NOT NULL,
  reservation_key VARCHAR(10) NOT NULL
);

INSERT INTO categories VALUES
(1, "Broken Screen"),
(2, "Loss of Data"),
(3, "Signs of Virus"),
(4, "Not Charging"),
(5, "Other");

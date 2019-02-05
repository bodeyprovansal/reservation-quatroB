DROP DATABASE IF EXISTS `warehouse`;
CREATE SCHEMA `warehouse`;
use `warehouse`;

CREATE TABLE IF NOT EXISTS `warehouse`.`categories` (
  `category_id` INT NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`category_id`));

CREATE TABLE IF NOT EXISTS `warehouse`.`customers` (
  `customer_id` INT NOT NULL,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `phone_number` VARCHAR(50) NOT NULL,
  `email_address` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`customer_id`));

CREATE TABLE IF NOT EXISTS `warehouse`.`orders` (
  `order_id` INT NOT NULL,
  `detailed_description` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`order_id`));

CREATE TABLE IF NOT EXISTS `warehouse`.`reservations` (
  `reservation_id` INT NOT NULL,
  `reservation_key` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`reservation_id`));

CREATE TABLE IF NOT EXISTS `warehouse`.`time` (
  `time_id` INT NOT NULL,
  `year` INT NOT NULL,
  `month` INT NOT NULL,
  `dayofweek` INT NOT NULL,
  `hour` INT NOT NULL,
  PRIMARY KEY (`time_id`));

CREATE TABLE IF NOT EXISTS `warehouse`.`fact` (
  `order_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `reservation_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  `time_id` INT NOT NULL,
  INDEX `fk_fact_categories_idx` (`category_id` ASC),
  INDEX `fk_fact_customers_idx` (`customer_id` ASC),
  INDEX `fk_fact_orders_idx` (`order_id` ASC),
  INDEX `fk_fact_time_idx` (`time_id` ASC),
  INDEX `fk_fact_reservations_idx` (`reservation_id` ASC),
  CONSTRAINT `fk_fact_categories`
    FOREIGN KEY (`category_id`)
    REFERENCES `warehouse`.`categories` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_fact_customers`
    FOREIGN KEY (`customer_id`)
    REFERENCES `warehouse`.`customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_fact_orders`
    FOREIGN KEY (`order_id`)
    REFERENCES `warehouse`.`orders` (`order_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_fact_time`
    FOREIGN KEY (`time_id`)
    REFERENCES `warehouse`.`time` (`time_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_fact_reservations`
    FOREIGN KEY (`reservation_id`)
    REFERENCES `warehouse`.`reservations` (`reservation_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

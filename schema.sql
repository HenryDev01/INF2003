-- Updated schema.sql

-- COPY PASTE THE STATEMENTS BELOW TO CREATE THE DATABASE

DROP DATABASE Project;

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS Project;

-- Switch to the Project database
USE Project;

-- Category Translation
CREATE TABLE Category_Translation (
    product_category_translation VARCHAR(255) PRIMARY KEY,
    product_category              VARCHAR(100) UNIQUE
);

-- Seller
CREATE TABLE Seller (
    seller_id        CHAR(32) PRIMARY KEY,
    seller_zip_code  VARCHAR(20),
    username         VARCHAR(100) UNIQUE,
    password_hash    CHAR(64)
);

-- Product
CREATE TABLE Product (
    product_id                    CHAR(32) PRIMARY KEY,
    product_category_translation  VARCHAR(255),
    product_name                  VARCHAR(100),
    product_weight_g              FLOAT,
    product_length_cm             FLOAT,
    product_height_cm             FLOAT,
    product_width_cm              FLOAT,
    product_photo                 VARCHAR(255),
    has_stock                     BOOLEAN,
    product_description           TEXT,
    product_model                 VARCHAR(50),
    price                         DECIMAL(10, 2),
    seller_id                     VARCHAR(255),
    FOREIGN KEY (product_category_translation) REFERENCES Category_Translation(product_category_translation),
    FOREIGN KEY (seller_id) REFERENCES Seller(seller_id)
);

-- Customer
CREATE TABLE Customer (
    customer_id        CHAR(32) PRIMARY KEY,
    customer_zip_code  VARCHAR(20),
    username           VARCHAR(100) UNIQUE,
    password_hash      CHAR(64),
    name               VARCHAR(100),
    contact            VARCHAR(20),
    email              VARCHAR(100) UNIQUE,
    photo              VARCHAR(255)
);

-- Order
CREATE TABLE Orders (
    order_id                      CHAR(32) PRIMARY KEY,
    customer_id                   CHAR(32),
    order_status                  VARCHAR(20),
    order_purchase_timestamp      DATETIME,
    order_approved_at             DATETIME,
    order_delivery_carrier_date   DATETIME,
    order_delivery_customer_date  DATETIME,
    order_estimated_delivery_date DATETIME,
    order_cancellation_reason     VARCHAR(255),
    shipping_address              VARCHAR(255),
    shipping_postal_code          VARCHAR(20),
    city                          VARCHAR(100),
    state                         VARCHAR(50),,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- Order Items
CREATE TABLE Order_Items (
    order_id            CHAR(32),
    order_item_id       INT,
    product_id          CHAR(32),
    seller_id           CHAR(32),
    shipping_limit_date DATETIME,
    price               DECIMAL(10, 2),
    freight_value       FLOAT,
    PRIMARY KEY (order_id, order_item_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    FOREIGN KEY (seller_id) REFERENCES Seller(seller_id)
);

-- Payment
CREATE TABLE Payment (
    order_id      CHAR(32),
    payment_type  VARCHAR(30),
    payment_value DECIMAL(10, 2),
    PRIMARY KEY (order_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

create table Admin (
    admin_id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255)
);

DROP TRIGGER IF EXISTS auto_update_order_timestamps;

DELIMITER $$
CREATE TRIGGER auto_update_order_timestamps
BEFORE UPDATE ON Orders
FOR EACH ROW
BEGIN
    IF OLD.order_status != 'Processing' AND NEW.order_status = 'Processing' THEN
        SET NEW.order_approved_at = NOW();
    END IF;

    IF (OLD.order_status != 'Packed' AND NEW.order_status = 'Packed') OR
       (OLD.order_status != 'Shipped' AND NEW.order_status = 'Shipped') THEN
        SET NEW.order_delivery_carrier_date = NOW();
    END IF;

    IF OLD.order_status != 'Delivered' AND NEW.order_status = 'Delivered' THEN
        SET NEW.order_delivery_customer_date = NOW();
    END IF;
END$$
DELIMITER ;
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
    product_category                    VARCHAR(255)
);

-- Product
CREATE TABLE Product (
    product_id              VARCHAR(255) PRIMARY KEY,
    product_category_translation VARCHAR(255),
    product_name            VARCHAR(255),
    product_weight_g        FLOAT,
    product_length_cm       FLOAT,
    product_height_cm       FLOAT,
    product_width_cm        FLOAT,
    product_photo           VARCHAR(255),
    has_stock               TINYINT(1),
    product_description     VARCHAR(255),
    product_model           VARCHAR(50),
    price               DECIMAL(10, 2),
    FOREIGN KEY (product_category_translation) REFERENCES Category_Translation(product_category_translation)
);

-- Seller
CREATE TABLE Seller (
    seller_id               VARCHAR(255) PRIMARY KEY,
    seller_zip_code         VARCHAR(20),
    username                VARCHAR(255),
    password_hash           VARCHAR(255)
);

-- Customer
CREATE TABLE Customer (
    customer_id             VARCHAR(255) PRIMARY KEY,
    customer_zip_code       VARCHAR(20),
    username                VARCHAR(255),
    password_hash           VARCHAR(255),
    name                    VARCHAR(100),
    contact                 VARCHAR(20),
    email                   VARCHAR(100),
    photo                   VARCHAR(255)
);

-- Order
CREATE TABLE Orders(
    order_id                        VARCHAR(255) PRIMARY KEY,
    customer_id                     VARCHAR(255),
    order_status                    VARCHAR(50),
    order_purchase_timestamp        DATETIME,
    order_approved_at               DATETIME,
    order_delivery_carrier_date     DATETIME,
    order_delivery_customer_date    DATETIME,
    order_estimated_delivery_date   DATETIME,
    order_cancellation_reason       VARCHAR(255),
    shipping_address               VARCHAR(255),
    shipping_postal_code            VARCHAR(20),
    city                            VARCHAR(100),
    state                           VARCHAR(2),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- Order Items
CREATE TABLE Order_Items (
    order_id            VARCHAR(255),
    order_item_id       INT,
    product_id          VARCHAR(255),
    seller_id           VARCHAR(255),
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
    order_id            VARCHAR(255),
    payment_type        VARCHAR(50),
    payment_value       DOUBLE,
    PRIMARY KEY (order_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);
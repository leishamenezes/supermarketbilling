CREATE DATABASE EssentialsMart;
 
-- Use the database
USE EssentialsMart;
 
-- Create the Products table
CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255),
    price DECIMAL(10, 2),
    stock_quantity INT
);
 
-- Create the Billing table
CREATE TABLE Billing (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    total_amount DECIMAL(10, 2),
    billing_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
 
-- Create the BillingDetails table
CREATE TABLE BillingDetails (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT,
    customer_name VARCHAR(255),
    product_id INT,
    quantity INT,
    price_per_item DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    FOREIGN KEY (bill_id) REFERENCES Billing(bill_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

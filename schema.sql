-- Sales Data Pipeline Database Schema
-- Create database and table for sales data

-- Create database (if it doesn't exist)
CREATE DATABASE IF NOT EXISTS sales_db;
USE sales_db;

-- Create sales table
CREATE TABLE IF NOT EXISTS sales (
    order_id VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    product VARCHAR(100) NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    price_per_unit DECIMAL(10, 2) NOT NULL CHECK (price_per_unit >= 0),
    total_price DECIMAL(10, 2) NOT NULL CHECK (total_price >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (order_id),
    INDEX idx_date (date),
    INDEX idx_customer (customer_name),
    INDEX idx_product (product)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create view for daily sales summary
CREATE OR REPLACE VIEW daily_sales_summary AS
SELECT 
    date,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_name) AS unique_customers,
    SUM(quantity) AS total_quantity_sold,
    SUM(total_price) AS daily_revenue,
    AVG(total_price) AS avg_order_value
FROM sales
GROUP BY date
ORDER BY date DESC;

-- Create view for product performance
CREATE OR REPLACE VIEW product_performance AS
SELECT 
    product,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_quantity_sold,
    SUM(total_price) AS total_revenue,
    AVG(price_per_unit) AS avg_price,
    MIN(price_per_unit) AS min_price,
    MAX(price_per_unit) AS max_price
FROM sales
GROUP BY product
ORDER BY total_revenue DESC;

-- SQL Analysis Project Schema
-- Purpose: Demonstrate SQL skills by analyzing sales data

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    price REAL
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    sale_date DATE,
    quantity INTEGER,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Insert Sample Data
INSERT INTO products (product_id, product_name, category, price) VALUES
(1, 'Laptop', 'Electronics', 1200.00),
(2, 'Headphones', 'Electronics', 150.00),
(3, 'Coffee Maker', 'Appliances', 80.00),
(4, 'Office Chair', 'Furniture', 200.00);

INSERT INTO sales (product_id, sale_date, quantity) VALUES
(1, '2023-01-15', 2),
(2, '2023-01-16', 5),
(3, '2023-01-17', 1),
(1, '2023-02-01', 1),
(4, '2023-02-05', 3);

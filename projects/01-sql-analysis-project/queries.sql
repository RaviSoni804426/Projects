-- Analysis Queries

-- 1. Total Revenue per Product
SELECT 
    p.product_name, 
    SUM(s.quantity * p.price) as total_revenue
FROM products p
JOIN sales s ON p.product_id = s.product_id
GROUP BY p.product_name
ORDER BY total_revenue DESC;

-- 2. Sales Trend (Count of sales per month)
SELECT 
    strftime('%Y-%m', sale_date) as month,
    COUNT(*) as number_of_sales
FROM sales
GROUP BY month;

-- 3. Top Selling Category
SELECT 
    p.category,
    SUM(s.quantity) as total_quantity
FROM products p
JOIN sales s ON p.product_id = s.product_id
GROUP BY p.category
ORDER BY total_quantity DESC
LIMIT 1;

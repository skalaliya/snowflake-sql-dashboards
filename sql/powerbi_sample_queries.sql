-- Sample Power BI Queries for Snowflake Analytics Platform
-- Copy these into Power BI's Query Editor for testing

-- 1. Executive Summary KPIs
SELECT 
    COUNT(DISTINCT O_CUSTKEY) as total_customers,
    COUNT(DISTINCT O_ORDERKEY) as total_orders,
    SUM(PRICE_AFTER_DISCOUNT) as total_revenue,
    AVG(PRICE_AFTER_DISCOUNT) as avg_order_value,
    SUM(L_QUANTITY) as total_quantity_sold
FROM CUSTOMER_LINEITEM_PROFILE;

-- 2. Monthly Revenue Trend
SELECT 
    DATE_TRUNC('MONTH', O_ORDERDATE) as order_month,
    COUNT(DISTINCT O_ORDERKEY) as monthly_orders,
    SUM(PRICE_AFTER_DISCOUNT) as monthly_revenue,
    COUNT(DISTINCT O_CUSTKEY) as monthly_customers
FROM CUSTOMER_LINEITEM_PROFILE
GROUP BY DATE_TRUNC('MONTH', O_ORDERDATE)
ORDER BY order_month;

-- 3. Order Status Performance
SELECT 
    O_ORDERSTATUS as order_status,
    COUNT(DISTINCT O_CUSTKEY) as customers,
    COUNT(DISTINCT O_ORDERKEY) as orders,
    SUM(PRICE_AFTER_DISCOUNT) as revenue,
    AVG(PRICE_PER_QTY) as avg_price_per_qty,
    SUM(L_QUANTITY) as total_quantity
FROM CUSTOMER_LINEITEM_PROFILE
GROUP BY O_ORDERSTATUS
ORDER BY revenue DESC;

-- 4. Top Customers by Revenue
SELECT 
    O_CUSTKEY as customer_id,
    COUNT(DISTINCT O_ORDERKEY) as order_count,
    SUM(PRICE_AFTER_DISCOUNT) as total_revenue,
    AVG(PRICE_AFTER_DISCOUNT) as avg_order_value,
    MIN(O_ORDERDATE) as first_order_date,
    MAX(O_ORDERDATE) as last_order_date
FROM CUSTOMER_LINEITEM_PROFILE
GROUP BY O_CUSTKEY
ORDER BY total_revenue DESC
LIMIT 100;

-- 5. Yearly Performance Comparison
SELECT 
    YEAR(O_ORDERDATE) as order_year,
    COUNT(DISTINCT O_CUSTKEY) as annual_customers,
    COUNT(DISTINCT O_ORDERKEY) as annual_orders,
    SUM(PRICE_AFTER_DISCOUNT) as annual_revenue,
    SUM(L_QUANTITY) as annual_quantity
FROM CUSTOMER_LINEITEM_PROFILE
GROUP BY YEAR(O_ORDERDATE)
ORDER BY order_year;

-- 6. Customer Segmentation by Order Frequency
SELECT 
    CASE 
        WHEN order_count >= 20 THEN 'High Frequency (20+)'
        WHEN order_count >= 10 THEN 'Medium Frequency (10-19)'
        WHEN order_count >= 5 THEN 'Regular (5-9)'
        ELSE 'Low Frequency (1-4)'
    END as customer_segment,
    COUNT(*) as customer_count,
    SUM(total_revenue) as segment_revenue,
    AVG(total_revenue) as avg_customer_value
FROM (
    SELECT 
        O_CUSTKEY,
        COUNT(DISTINCT O_ORDERKEY) as order_count,
        SUM(PRICE_AFTER_DISCOUNT) as total_revenue
    FROM CUSTOMER_LINEITEM_PROFILE
    GROUP BY O_CUSTKEY
) customer_summary
GROUP BY customer_segment
ORDER BY avg_customer_value DESC;

-- 7. Price Analysis by Quantity Ranges
SELECT 
    CASE 
        WHEN L_QUANTITY >= 50 THEN 'Bulk (50+)'
        WHEN L_QUANTITY >= 25 THEN 'Large (25-49)'
        WHEN L_QUANTITY >= 10 THEN 'Medium (10-24)'
        ELSE 'Small (1-9)'
    END as quantity_range,
    COUNT(*) as line_item_count,
    SUM(PRICE_AFTER_DISCOUNT) as total_revenue,
    AVG(PRICE_PER_QTY) as avg_price_per_qty,
    SUM(L_QUANTITY) as total_quantity
FROM CUSTOMER_LINEITEM_PROFILE
GROUP BY quantity_range
ORDER BY total_revenue DESC;

-- 8. Order Value Distribution
SELECT 
    CASE 
        WHEN order_value >= 100000 THEN '$100K+'
        WHEN order_value >= 50000 THEN '$50K-$100K'
        WHEN order_value >= 25000 THEN '$25K-$50K'
        WHEN order_value >= 10000 THEN '$10K-$25K'
        WHEN order_value >= 5000 THEN '$5K-$10K'
        ELSE 'Under $5K'
    END as order_value_range,
    COUNT(*) as order_count,
    SUM(order_value) as total_revenue,
    AVG(order_value) as avg_order_value
FROM (
    SELECT 
        O_ORDERKEY,
        SUM(PRICE_AFTER_DISCOUNT) as order_value
    FROM CUSTOMER_LINEITEM_PROFILE
    GROUP BY O_ORDERKEY
) order_summary
GROUP BY order_value_range
ORDER BY avg_order_value DESC;

-- 9. Date Range Analysis for Filtering
SELECT 
    MIN(O_ORDERDATE) as earliest_date,
    MAX(O_ORDERDATE) as latest_date,
    COUNT(DISTINCT DATE_TRUNC('YEAR', O_ORDERDATE)) as years_of_data,
    COUNT(DISTINCT DATE_TRUNC('MONTH', O_ORDERDATE)) as months_of_data,
    COUNT(DISTINCT O_ORDERDATE) as distinct_order_dates
FROM CUSTOMER_LINEITEM_PROFILE;

-- 10. Performance Test Query (for DirectQuery validation)
SELECT 
    O_ORDERSTATUS,
    COUNT(*) as record_count,
    COUNT(DISTINCT O_CUSTKEY) as customer_count,
    COUNT(DISTINCT O_ORDERKEY) as order_count,
    SUM(PRICE_AFTER_DISCOUNT) as total_revenue
FROM CUSTOMER_LINEITEM_PROFILE
GROUP BY O_ORDERSTATUS;
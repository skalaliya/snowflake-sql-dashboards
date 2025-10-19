-- Looker Setup SQL for Snowflake Analytics Platform
-- Complete setup for both Looker Studio and Looker Cloud

-- =============================================================================
-- 1. DEDICATED LOOKER ROLE AND PERMISSIONS
-- =============================================================================

-- Create Looker-specific role (least privilege)
CREATE ROLE IF NOT EXISTS LOOKER_ROLE
  COMMENT = 'Role for Looker BI tool access to analytics data';

-- Grant warehouse access with auto-resume capability
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE LOOKER_ROLE;
GRANT OPERATE ON WAREHOUSE COMPUTE_WH TO ROLE LOOKER_ROLE;

-- Grant database and schema access
GRANT USAGE ON DATABASE TPCH_DASHBOARDS TO ROLE LOOKER_ROLE;
GRANT USAGE ON SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE LOOKER_ROLE;

-- Grant read access to all existing tables and views
GRANT SELECT ON ALL TABLES IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE LOOKER_ROLE;
GRANT SELECT ON ALL VIEWS IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE LOOKER_ROLE;

-- Grant access to future tables and views (important for CI/CD)
GRANT SELECT ON FUTURE TABLES IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE LOOKER_ROLE;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE LOOKER_ROLE;

-- =============================================================================
-- 2. DEDICATED LOOKER USER (OPTIONAL BUT RECOMMENDED)
-- =============================================================================

-- Create service user for Looker connections
CREATE USER IF NOT EXISTS LOOKER_USER
  PASSWORD = 'LookerSecure2024!'
  DEFAULT_ROLE = LOOKER_ROLE
  DEFAULT_WAREHOUSE = COMPUTE_WH
  DEFAULT_NAMESPACE = TPCH_DASHBOARDS.PUBLIC
  MUST_CHANGE_PASSWORD = TRUE
  COMMENT = 'Service user for Looker BI tool connections';

-- Grant role to user
GRANT ROLE LOOKER_ROLE TO USER LOOKER_USER;

-- Also grant to main user for flexibility
GRANT ROLE LOOKER_ROLE TO USER ALGORYTHMOS;

-- =============================================================================
-- 3. LOOKER-OPTIMIZED VIEWS (FOR BETTER PERFORMANCE)
-- =============================================================================

-- Monthly revenue summary (optimized for Looker time series)
CREATE OR REPLACE VIEW V_LOOKER_MONTHLY_REVENUE AS
SELECT 
    DATE_TRUNC('MONTH', O_ORDERDATE) as MONTH,
    O_ORDERSTATUS as ORDER_STATUS,
    COUNT(DISTINCT O_CUSTKEY) as MONTHLY_CUSTOMERS,
    COUNT(DISTINCT O_ORDERKEY) as MONTHLY_ORDERS,
    SUM(PRICE_AFTER_DISCOUNT) as MONTHLY_REVENUE,
    AVG(PRICE_AFTER_DISCOUNT) as AVG_ORDER_VALUE,
    SUM(L_QUANTITY) as MONTHLY_QUANTITY
FROM CUSTOMER_LINEITEM_PROFILE
GROUP BY DATE_TRUNC('MONTH', O_ORDERDATE), O_ORDERSTATUS
ORDER BY MONTH DESC;

-- Customer summary (optimized for Looker customer analysis)
CREATE OR REPLACE VIEW V_LOOKER_CUSTOMER_SUMMARY AS
SELECT 
    O_CUSTKEY as CUSTOMER_ID,
    COUNT(DISTINCT O_ORDERKEY) as TOTAL_ORDERS,
    SUM(PRICE_AFTER_DISCOUNT) as TOTAL_REVENUE,
    AVG(PRICE_AFTER_DISCOUNT) as AVG_ORDER_VALUE,
    MIN(O_ORDERDATE) as FIRST_ORDER_DATE,
    MAX(O_ORDERDATE) as LAST_ORDER_DATE,
    DATEDIFF(DAY, MIN(O_ORDERDATE), MAX(O_ORDERDATE)) as CUSTOMER_LIFESPAN_DAYS,
    SUM(L_QUANTITY) as TOTAL_QUANTITY_PURCHASED
FROM CUSTOMER_LINEITEM_PROFILE
GROUP BY O_CUSTKEY;

-- Daily metrics (for real-time dashboards)
CREATE OR REPLACE VIEW V_LOOKER_DAILY_METRICS AS
SELECT 
    O_ORDERDATE as ORDER_DATE,
    O_ORDERSTATUS as ORDER_STATUS,
    COUNT(DISTINCT O_CUSTKEY) as DAILY_CUSTOMERS,
    COUNT(DISTINCT O_ORDERKEY) as DAILY_ORDERS,
    SUM(PRICE_AFTER_DISCOUNT) as DAILY_REVENUE,
    SUM(L_QUANTITY) as DAILY_QUANTITY
FROM CUSTOMER_LINEITEM_PROFILE
GROUP BY O_ORDERDATE, O_ORDERSTATUS
ORDER BY ORDER_DATE DESC;

-- =============================================================================
-- 4. GRANT ACCESS TO NEW LOOKER VIEWS
-- =============================================================================

GRANT SELECT ON V_LOOKER_MONTHLY_REVENUE TO ROLE LOOKER_ROLE;
GRANT SELECT ON V_LOOKER_CUSTOMER_SUMMARY TO ROLE LOOKER_ROLE;
GRANT SELECT ON V_LOOKER_DAILY_METRICS TO ROLE LOOKER_ROLE;

-- =============================================================================
-- 5. LOOKER STUDIO CONNECTION TEST QUERIES
-- =============================================================================

-- Test query 1: Basic connectivity
-- SELECT COUNT(*) as TOTAL_RECORDS FROM CUSTOMER_LINEITEM_PROFILE;

-- Test query 2: Monthly revenue trend (good for line charts)
-- SELECT 
--     DATE_TRUNC('MONTH', O_ORDERDATE) as MONTH,
--     SUM(PRICE_AFTER_DISCOUNT) as REVENUE
-- FROM CUSTOMER_LINEITEM_PROFILE
-- GROUP BY MONTH
-- ORDER BY MONTH;

-- Test query 3: Top customers (good for tables/bar charts)
-- SELECT 
--     O_CUSTKEY as CUSTOMER_ID,
--     SUM(PRICE_AFTER_DISCOUNT) as TOTAL_REVENUE
-- FROM CUSTOMER_LINEITEM_PROFILE
-- GROUP BY CUSTOMER_ID
-- ORDER BY TOTAL_REVENUE DESC
-- LIMIT 10;

-- =============================================================================
-- 6. PERFORMANCE OPTIMIZATION FOR LOOKER
-- =============================================================================

-- Enable result caching for better Looker performance
ALTER SESSION SET USE_CACHED_RESULT = TRUE;

-- Set query timeout for long-running Looker queries
ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 3600;

-- Optimize warehouse for BI workloads
-- (Run as ACCOUNTADMIN if needed)
-- ALTER WAREHOUSE COMPUTE_WH SET 
--   AUTO_SUSPEND = 60
--   AUTO_RESUME = TRUE
--   INITIALLY_SUSPENDED = FALSE;

-- =============================================================================
-- 7. VERIFICATION AND TESTING
-- =============================================================================

-- Verify Looker role permissions
SHOW GRANTS TO ROLE LOOKER_ROLE;

-- Verify user creation
SHOW USERS LIKE 'LOOKER_USER';

-- Test data access as Looker user
USE ROLE LOOKER_ROLE;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE TPCH_DASHBOARDS;
USE SCHEMA PUBLIC;

-- Validate main data sources
SELECT 'CUSTOMER_LINEITEM_PROFILE' as TABLE_NAME, COUNT(*) as ROW_COUNT FROM CUSTOMER_LINEITEM_PROFILE
UNION ALL
SELECT 'V_CUSTOMER_DETAILS', COUNT(*) FROM V_CUSTOMER_DETAILS
UNION ALL
SELECT 'V_ORDER_DETAILS', COUNT(*) FROM V_ORDER_DETAILS
UNION ALL
SELECT 'V_MONTHLY_REVENUE_BY_REGION', COUNT(*) FROM V_MONTHLY_REVENUE_BY_REGION
UNION ALL
SELECT 'V_MARKET_SEGMENT_ANALYSIS', COUNT(*) FROM V_MARKET_SEGMENT_ANALYSIS
UNION ALL
SELECT 'V_LOOKER_MONTHLY_REVENUE', COUNT(*) FROM V_LOOKER_MONTHLY_REVENUE
UNION ALL
SELECT 'V_LOOKER_CUSTOMER_SUMMARY', COUNT(*) FROM V_LOOKER_CUSTOMER_SUMMARY
UNION ALL
SELECT 'V_LOOKER_DAILY_METRICS', COUNT(*) FROM V_LOOKER_DAILY_METRICS;

-- =============================================================================
-- SUMMARY: LOOKER SETUP COMPLETE!
-- =============================================================================

/*
✅ LOOKER CONNECTION READY!

Connection Details for Looker Studio & Looker Cloud:
────────────────────────────────────────────────────
Server: JHYWOUK-WA83239.snowflakecomputing.com
Database: TPCH_DASHBOARDS
Schema: PUBLIC
Warehouse: COMPUTE_WH
Username: LOOKER_USER (or ALGORYTHMOS)
Password: LookerSecure2024! (change this!)
Role: LOOKER_ROLE

Available Data Sources:
─────────────────────
📊 CUSTOMER_LINEITEM_PROFILE (4.5M+ records) - Main fact table
👥 V_CUSTOMER_DETAILS (150K records) - Customer demographics
📦 V_ORDER_DETAILS (1.5M records) - Order summaries
🌍 V_MONTHLY_REVENUE_BY_REGION (400 records) - Regional analysis
📈 V_MARKET_SEGMENT_ANALYSIS (25 records) - Market segments
📅 V_LOOKER_MONTHLY_REVENUE (optimized for time series)
🎯 V_LOOKER_CUSTOMER_SUMMARY (optimized for customer analysis)
📊 V_LOOKER_DAILY_METRICS (optimized for real-time dashboards)

Looker Studio Setup:
──────────────────
1. Go to lookerstudio.google.com
2. Create → Data source → Search "Snowflake"
3. Enter connection details above
4. Select tables/views you want
5. Create report and start visualizing!

Looker Cloud Setup:
─────────────────
1. Import the LookML model from config/looker_model.lkml
2. Create connection with details above
3. Deploy to production
4. Start exploring your data!

🚀 Your Looker connection is ready for enterprise analytics!
*/
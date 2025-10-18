-- 04_tasks.sql
-- Scheduled Tasks for Dashboard Data Refresh
-- Example tasks for maintaining materialized views and refreshing aggregations

USE DATABASE TPCH_DASHBOARDS;
USE SCHEMA PUBLIC;

-- Note: Tasks are commented out by default to prevent unintended execution
-- Uncomment and modify as needed for your use case

-- Example 1: Daily refresh task for customer metrics
-- This task would refresh a materialized view or table daily at 2 AM UTC
/*
CREATE OR REPLACE TASK TASK_DAILY_CUSTOMER_REFRESH
    WAREHOUSE = ANALYTICS_WH
    SCHEDULE = 'USING CRON 0 2 * * * UTC'
    COMMENT = 'Daily refresh of customer metrics at 2 AM UTC'
AS
    -- Refresh logic would go here
    -- For example, creating a snapshot table:
    CREATE OR REPLACE TABLE CUSTOMER_METRICS_SNAPSHOT AS
    SELECT 
        CURRENT_TIMESTAMP() as SNAPSHOT_TIME,
        *
    FROM V_TOP_CUSTOMERS
    LIMIT 1000;
*/

-- Example 2: Hourly incremental refresh task
-- This task would run every hour to update recent data
/*
CREATE OR REPLACE TASK TASK_HOURLY_METRICS_UPDATE
    WAREHOUSE = ANALYTICS_WH
    SCHEDULE = 'USING CRON 0 * * * * UTC'
    COMMENT = 'Hourly update of real-time metrics'
AS
    -- Insert new records into a log table or update aggregations
    INSERT INTO ORDER_METRICS_LOG
    SELECT 
        CURRENT_TIMESTAMP() as LOG_TIME,
        COUNT(*) as TOTAL_ORDERS,
        SUM(O_TOTALPRICE) as TOTAL_REVENUE
    FROM V_ORDER_DETAILS
    WHERE O_ORDERDATE >= DATEADD(hour, -1, CURRENT_TIMESTAMP());
*/

-- Example 3: Weekly reporting task
-- This task would run weekly on Mondays at 8 AM UTC
/*
CREATE OR REPLACE TASK TASK_WEEKLY_REPORT_GENERATION
    WAREHOUSE = ANALYTICS_WH
    SCHEDULE = 'USING CRON 0 8 * * MON UTC'
    COMMENT = 'Weekly report generation every Monday at 8 AM UTC'
AS
    -- Generate weekly summary
    CREATE OR REPLACE TABLE WEEKLY_SUMMARY AS
    SELECT 
        DATE_TRUNC('WEEK', CURRENT_DATE()) as REPORT_WEEK,
        REGION,
        SUM(TOTAL_REVENUE) as WEEKLY_REVENUE,
        SUM(ORDER_COUNT) as WEEKLY_ORDERS
    FROM V_MONTHLY_REVENUE_BY_REGION
    WHERE ORDER_MONTH >= DATEADD(week, -1, CURRENT_DATE())
    GROUP BY REGION;
*/

-- Example 4: Task with dependency chain
-- Parent task that triggers child tasks
/*
CREATE OR REPLACE TASK TASK_PARENT_DATA_LOAD
    WAREHOUSE = ANALYTICS_WH
    SCHEDULE = 'USING CRON 0 0 * * * UTC'
    COMMENT = 'Parent task that loads data daily at midnight'
AS
    -- Load data from external source
    CREATE OR REPLACE TABLE STAGING_ORDERS AS
    SELECT * FROM V_ORDER_DETAILS
    WHERE O_ORDERDATE = CURRENT_DATE() - 1;

-- Child task that depends on parent
CREATE OR REPLACE TASK TASK_CHILD_DATA_TRANSFORM
    WAREHOUSE = ANALYTICS_WH
    AFTER TASK_PARENT_DATA_LOAD
    COMMENT = 'Child task that transforms data after parent completes'
AS
    -- Transform loaded data
    CREATE OR REPLACE TABLE PROCESSED_ORDERS AS
    SELECT 
        O_ORDERKEY,
        O_CUSTKEY,
        O_TOTALPRICE,
        DATE_TRUNC('MONTH', O_ORDERDATE) as ORDER_MONTH
    FROM STAGING_ORDERS;
*/

-- To enable a task (when uncommenting above), use:
-- ALTER TASK TASK_NAME RESUME;

-- To suspend a task, use:
-- ALTER TASK TASK_NAME SUSPEND;

-- To view task history:
-- SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY())
--   WHERE NAME = 'TASK_NAME'
--   ORDER BY SCHEDULED_TIME DESC;

-- Placeholder query to avoid empty execution
SELECT 'Tasks are commented out by default. Review and uncomment as needed.' as INFO;

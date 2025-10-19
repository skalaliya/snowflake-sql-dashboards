-- ============================================================================
-- Pipeline Prerequisites
-- ============================================================================
-- Uses current database/schema from connection (SNOW_DATABASE/SNOW_SCHEMA)
-- Grant sample data access for TPCH source reads

-- Grant sample data access for TPCH source reads
-- Use IMPORTED PRIVILEGES for shared databases like SNOWFLAKE_SAMPLE_DATA
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE_SAMPLE_DATA TO ROLE ACCOUNTADMIN;

-- Optional helper objects schema (if you want to separate):
-- CREATE SCHEMA IF NOT EXISTS HELPERS;
-- ============================================================================
-- Pipeline Prerequisites
-- ============================================================================
-- Uses current database/schema from connection (SNOW_DATABASE/SNOW_SCHEMA)
-- Grant sample data access for TPCH source reads

-- Grant sample data access for TPCH source reads
GRANT USAGE ON DATABASE SNOWFLAKE_SAMPLE_DATA TO ROLE IDENTIFIER(CURRENT_ROLE());
GRANT USAGE ON SCHEMA SNOWFLAKE_SAMPLE_DATA.TPCH_SF1 TO ROLE IDENTIFIER(CURRENT_ROLE());

-- Ensure we have SELECT privileges on the TPCH tables
GRANT SELECT ON ALL TABLES IN SCHEMA SNOWFLAKE_SAMPLE_DATA.TPCH_SF1 TO ROLE IDENTIFIER(CURRENT_ROLE());

-- Optional helper objects schema (if you want to separate):
-- CREATE SCHEMA IF NOT EXISTS HELPERS;
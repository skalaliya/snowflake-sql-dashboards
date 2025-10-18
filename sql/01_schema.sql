-- 01_schema.sql
-- Database and Schema Setup for TPCH Dashboards
-- This script creates the necessary database and schema structure

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS TPCH_DASHBOARDS
    COMMENT = 'Database for TPCH dashboard analytics';

-- Use the database
USE DATABASE TPCH_DASHBOARDS;

-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS PUBLIC
    COMMENT = 'Public schema for TPCH dashboard objects';

-- Use the schema
USE SCHEMA PUBLIC;

-- Create a warehouse for analytics if it doesn't exist
CREATE WAREHOUSE IF NOT EXISTS ANALYTICS_WH
    WITH WAREHOUSE_SIZE = 'SMALL'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Warehouse for TPCH dashboard analytics';

-- Display current context
SELECT CURRENT_DATABASE() as current_db, 
       CURRENT_SCHEMA() as current_schema,
       CURRENT_WAREHOUSE() as current_warehouse;

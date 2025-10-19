-- BI Security Setup for Snowflake Analytics Platform
-- Run these commands to create dedicated BI users and roles

-- =============================================================================
-- 1. CREATE DEDICATED BI ROLES
-- =============================================================================

-- Looker role with appropriate permissions
CREATE ROLE IF NOT EXISTS LOOKER_ROLE;

-- Power BI role 
CREATE ROLE IF NOT EXISTS POWERBI_ROLE;

-- Tableau role
CREATE ROLE IF NOT EXISTS TABLEAU_ROLE;

-- General BI role (if you prefer one role for all tools)
CREATE ROLE IF NOT EXISTS BI_ROLE;

-- =============================================================================
-- 2. GRANT WAREHOUSE ACCESS
-- =============================================================================

-- Looker permissions
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE LOOKER_ROLE;
GRANT OPERATE ON WAREHOUSE COMPUTE_WH TO ROLE LOOKER_ROLE; -- Auto-resume capability

-- Power BI permissions
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE POWERBI_ROLE;
GRANT OPERATE ON WAREHOUSE COMPUTE_WH TO ROLE POWERBI_ROLE;

-- Tableau permissions
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE TABLEAU_ROLE;
GRANT OPERATE ON WAREHOUSE COMPUTE_WH TO ROLE TABLEAU_ROLE;

-- General BI permissions
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE BI_ROLE;
GRANT OPERATE ON WAREHOUSE COMPUTE_WH TO ROLE BI_ROLE;

-- =============================================================================
-- 3. GRANT DATABASE AND SCHEMA ACCESS
-- =============================================================================

-- Looker database access
GRANT USAGE ON DATABASE TPCH_DASHBOARDS TO ROLE LOOKER_ROLE;
GRANT USAGE ON SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE LOOKER_ROLE;

-- Power BI database access
GRANT USAGE ON DATABASE TPCH_DASHBOARDS TO ROLE POWERBI_ROLE;
GRANT USAGE ON SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE POWERBI_ROLE;

-- Tableau database access
GRANT USAGE ON DATABASE TPCH_DASHBOARDS TO ROLE TABLEAU_ROLE;
GRANT USAGE ON SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE TABLEAU_ROLE;

-- General BI database access
GRANT USAGE ON DATABASE TPCH_DASHBOARDS TO ROLE BI_ROLE;
GRANT USAGE ON SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE BI_ROLE;

-- =============================================================================
-- 4. GRANT TABLE AND VIEW ACCESS
-- =============================================================================

-- Looker data access
GRANT SELECT ON ALL TABLES IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE LOOKER_ROLE;
GRANT SELECT ON ALL VIEWS IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE LOOKER_ROLE;
GRANT SELECT ON FUTURE TABLES IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE LOOKER_ROLE;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE LOOKER_ROLE;

-- Power BI data access
GRANT SELECT ON ALL TABLES IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE POWERBI_ROLE;
GRANT SELECT ON ALL VIEWS IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE POWERBI_ROLE;
GRANT SELECT ON FUTURE TABLES IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE POWERBI_ROLE;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE POWERBI_ROLE;

-- Tableau data access
GRANT SELECT ON ALL TABLES IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE TABLEAU_ROLE;
GRANT SELECT ON ALL VIEWS IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE TABLEAU_ROLE;
GRANT SELECT ON FUTURE TABLES IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE TABLEAU_ROLE;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE TABLEAU_ROLE;

-- General BI data access
GRANT SELECT ON ALL TABLES IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE BI_ROLE;
GRANT SELECT ON ALL VIEWS IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE BI_ROLE;
GRANT SELECT ON FUTURE TABLES IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE BI_ROLE;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA TPCH_DASHBOARDS.PUBLIC TO ROLE BI_ROLE;

-- =============================================================================
-- 5. CREATE DEDICATED BI USERS (OPTIONAL BUT RECOMMENDED)
-- =============================================================================

-- Looker service user
CREATE USER IF NOT EXISTS LOOKER_USER
  PASSWORD = 'LookerSecure2024!'
  DEFAULT_ROLE = LOOKER_ROLE
  DEFAULT_WAREHOUSE = COMPUTE_WH
  DEFAULT_NAMESPACE = TPCH_DASHBOARDS.PUBLIC
  COMMENT = 'Dedicated user for Looker BI connections';

-- Power BI service user
CREATE USER IF NOT EXISTS POWERBI_USER
  PASSWORD = 'PowerBISecure2024!'
  DEFAULT_ROLE = POWERBI_ROLE
  DEFAULT_WAREHOUSE = COMPUTE_WH
  DEFAULT_NAMESPACE = TPCH_DASHBOARDS.PUBLIC
  COMMENT = 'Dedicated user for Power BI connections';

-- Tableau service user
CREATE USER IF NOT EXISTS TABLEAU_USER
  PASSWORD = 'TableauSecure2024!'
  DEFAULT_ROLE = TABLEAU_ROLE
  DEFAULT_WAREHOUSE = COMPUTE_WH
  DEFAULT_NAMESPACE = TPCH_DASHBOARDS.PUBLIC
  COMMENT = 'Dedicated user for Tableau connections';

-- General BI service user
CREATE USER IF NOT EXISTS BI_USER
  PASSWORD = 'BIToolsSecure2024!'
  DEFAULT_ROLE = BI_ROLE
  DEFAULT_WAREHOUSE = COMPUTE_WH
  DEFAULT_NAMESPACE = TPCH_DASHBOARDS.PUBLIC
  COMMENT = 'General user for all BI tool connections';

-- =============================================================================
-- 6. ASSIGN ROLES TO USERS
-- =============================================================================

-- Grant roles to service users
GRANT ROLE LOOKER_ROLE TO USER LOOKER_USER;
GRANT ROLE POWERBI_ROLE TO USER POWERBI_USER;
GRANT ROLE TABLEAU_ROLE TO USER TABLEAU_USER;
GRANT ROLE BI_ROLE TO USER BI_USER;

-- Grant roles to your main user (ALGORYTHMOS) for flexibility
GRANT ROLE LOOKER_ROLE TO USER ALGORYTHMOS;
GRANT ROLE POWERBI_ROLE TO USER ALGORYTHMOS;
GRANT ROLE TABLEAU_ROLE TO USER ALGORYTHMOS;
GRANT ROLE BI_ROLE TO USER ALGORYTHMOS;

-- =============================================================================
-- 7. VERIFICATION QUERIES
-- =============================================================================

-- Check created roles
SHOW ROLES LIKE '%_ROLE';

-- Check created users
SHOW USERS LIKE '%_USER';

-- Test data access (run as each BI role)
-- USE ROLE LOOKER_ROLE;
-- SELECT COUNT(*) FROM CUSTOMER_LINEITEM_PROFILE;

-- =============================================================================
-- 8. NETWORK POLICIES (OPTIONAL - FOR PRODUCTION)
-- =============================================================================

-- Uncomment and modify IP addresses as needed for production security
/*
-- Create network policy for BI tools (replace with your actual IPs)
CREATE NETWORK POLICY BI_TOOLS_POLICY
  ALLOWED_IP_LIST=(
    '192.168.1.0/24',  -- Your office network
    '10.0.0.0/8'       -- Your cloud provider network
  )
  COMMENT='Network policy for BI tool connections';

-- Apply to BI users
ALTER USER LOOKER_USER SET NETWORK_POLICY = 'BI_TOOLS_POLICY';
ALTER USER POWERBI_USER SET NETWORK_POLICY = 'BI_TOOLS_POLICY';
ALTER USER TABLEAU_USER SET NETWORK_POLICY = 'BI_TOOLS_POLICY';
ALTER USER BI_USER SET NETWORK_POLICY = 'BI_TOOLS_POLICY';
*/

-- =============================================================================
-- SUMMARY: Your BI Security Setup is Complete!
-- =============================================================================

/*
You now have:
✅ Dedicated roles for each BI tool (LOOKER_ROLE, POWERBI_ROLE, TABLEAU_ROLE, BI_ROLE)
✅ Service users with appropriate permissions
✅ Least-privilege access to your analytics data
✅ Future-proofed permissions for new tables/views
✅ Warehouse auto-resume capabilities

Connection Details:
- Server: JHYWOUK-WA83239.snowflakecomputing.com
- Database: TPCH_DASHBOARDS
- Schema: PUBLIC
- Warehouse: COMPUTE_WH
- Users: LOOKER_USER, POWERBI_USER, TABLEAU_USER, or BI_USER
- Passwords: As set above (change them!)

Next Steps:
1. Change the default passwords above to secure ones
2. Use these credentials in your BI tool connections
3. Test connections with the provided test scripts
*/
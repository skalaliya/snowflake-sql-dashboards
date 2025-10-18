-- ============================================================================
-- Pipeline Cleanup
-- ============================================================================
-- Convenience teardown for demos

-- Suspend and drop the task
ALTER TASK IF EXISTS CUSTOMER_PROFILE_TASK SUSPEND;
DROP TASK IF EXISTS CUSTOMER_PROFILE_TASK;

-- Drop the stored procedure
DROP PROCEDURE IF EXISTS CREATE_CUSTOMER_PROFILE_SP();

-- Drop observability objects
DROP TABLE IF EXISTS PIPELINE_HEALTH;
DROP VIEW IF EXISTS V_TASK_HISTORY;

-- Keep CUSTOMER_LINEITEM_PROFILE if you want the data; otherwise:
-- DROP TABLE IF EXISTS CUSTOMER_LINEITEM_PROFILE;

-- Drop timestamped snapshots (example - adjust pattern as needed)
-- SHOW TABLES LIKE 'CUSTOMER_LINEITEM_PROFILE_%';
-- -- Then manually drop specific snapshots or use a loop in a stored procedure
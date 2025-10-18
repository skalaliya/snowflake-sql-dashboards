-- ============================================================================
-- Customer Profile Task
-- ============================================================================
-- Serverless task to refresh customer profiles from TPCH data
-- Tasks are created SUSPENDED by default (safe). Resume when ready.

CREATE OR REPLACE TASK CUSTOMER_PROFILE_TASK
SCHEDULE = 'USING CRON 0 * * * * UTC'  -- hourly at :00 UTC
COMMENT  = 'Refresh CUSTOMER_LINEITEM_PROFILE from TPCH demo data (serverless)'
AS
CALL CREATE_CUSTOMER_PROFILE_SP();

-- To run every 2 hours Paris time:
-- ALTER TASK CUSTOMER_PROFILE_TASK SET SCHEDULE = 'USING CRON 0 */2 * * * Europe/Paris';

-- When ready to activate:
-- ALTER TASK CUSTOMER_PROFILE_TASK RESUME;
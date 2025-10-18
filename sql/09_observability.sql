-- ============================================================================
-- Pipeline Observability
-- ============================================================================
-- Simple health artifacts: a table for freshness/rowcount and a view over task history

CREATE OR REPLACE TABLE PIPELINE_HEALTH (
  TS TIMESTAMP_TZ,
  ROWCOUNT NUMBER
);

-- Lightweight history view
CREATE OR REPLACE VIEW V_TASK_HISTORY AS
SELECT *
FROM TABLE(information_schema.task_history(
  scheduled_time_range_start => dateadd('day', -7, current_timestamp()),
  result_limit => 1000
));

-- Optional: add a post-run procedure to record counts;
-- or insert manually during ops:
-- INSERT INTO PIPELINE_HEALTH
-- SELECT CURRENT_TIMESTAMP(), COUNT(*) FROM CUSTOMER_LINEITEM_PROFILE;
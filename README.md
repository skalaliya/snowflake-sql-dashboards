# Snowflake SQL Dashboards

Production-ready Snowflake TPCH dashboards with automated CI/CD deployment and a complete Snowpark-pandas data pipeline. This repository contains numbered SQL files for schema setup, KPI views, aggregations, scheduled tasks, security grants, and a modern stored procedure + task pipeline that transforms TPCH data using Snowpark-pandas.

## 🚀 Features

- **Automated Deployment**: Hardened Python script with type hints, robust SQL parsing, and comprehensive error handling
- **TPCH Analytics**: Pre-built views and aggregations for Snowflake's sample TPCH data
- **CI/CD Integration**: GitHub Actions workflow for automatic deployment on push to main
- **Modern Data Pipeline**: Python stored procedure using Snowpark-pandas for TPCH data transformation
- **Serverless Tasks**: Automated data refresh with cron scheduling (created suspended for safety)
- **Observability**: Pipeline health monitoring and task history views
- **Security Best Practices**: Role-based access control with granular permissions
- **Flexible Execution**: Support for dry-run, selective file execution, and error handling modes

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions deployment workflow
├── scripts/
│   └── deploy.py                   # Hardened Python deployment script
├── sql/
│   ├── 01_schema.sql               # Database and schema setup
│   ├── 02_tpch_views.sql           # TPCH detail views
│   ├── 03_aggregations.sql         # KPI aggregations and metrics
│   ├── 04_tasks.sql                # Scheduled tasks (commented examples)
│   ├── 05_grants.sql               # Security grants and RBAC
│   ├── 06_pipeline_prereqs.sql     # Pipeline prerequisites and sample data grants
│   ├── 07_sp_customer_profile.sql  # Python stored procedure with Snowpark-pandas
│   ├── 08_task_customer_profile.sql# Serverless task for data pipeline
│   ├── 09_observability.sql        # Pipeline health monitoring
│   └── 10_cleanup.sql              # Demo cleanup script
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignore file
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🛠️ Setup Instructions

### Prerequisites

- Snowflake account with appropriate privileges
- Python 3.8 or higher
- Access to Snowflake's `SNOWFLAKE_SAMPLE_DATA` database (usually available by default)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/skalaliya/snowflake-sql-dashboards.git
   cd snowflake-sql-dashboards
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Snowflake credentials
   ```

4. **Update .env file with your Snowflake credentials**
   - `SNOW_ACCOUNT`: Your Snowflake account identifier (e.g., `xy12345.eu-west-1`)
   - `SNOW_USER`: Your Snowflake username  
   - `SNOW_PASSWORD`: Your Snowflake password
   - `SNOW_ROLE`: Role to use (e.g., `SYSADMIN`)
   - `SNOW_WAREHOUSE`: Warehouse to use (e.g., `TRANSFORM_WH`)
   - `SNOW_DATABASE`: Target database name (e.g., `ANALYTICS`)
   - `SNOW_SCHEMA`: Target schema name (e.g., `TPCH_APP`)

5. **Test the deployment script**
   ```bash
   # Dry run to see what would be executed
   python scripts/deploy.py --dry-run
   
   # Run with error stopping
   python scripts/deploy.py --stop-on-error
   
   # Run only a specific file
   python scripts/deploy.py --only 07_sp_customer_profile.sql
   ```

### GitHub Actions Setup

To enable automated deployment via GitHub Actions:

1. **Navigate to your repository settings**
   - Go to Settings → Secrets and variables → Actions

2. **Add the following secrets**:
   
   | Secret Name | Description | Example |
   |-------------|-------------|---------|
   | `SNOW_ACCOUNT` | Snowflake account identifier | `xy12345.us-east-1` |
   | `SNOW_USER` | Snowflake username | `DEPLOY_USER` |
   | `SNOW_PASSWORD` | Snowflake password | `your_secure_password` |
   | `SNOW_ROLE` | Snowflake role | `ACCOUNTADMIN` |
   | `SNOW_DATABASE` | Target database | `TPCH_DASHBOARDS` |
   | `SNOW_SCHEMA` | Target schema | `PUBLIC` |
   | `SNOW_WAREHOUSE` | Compute warehouse | `COMPUTE_WH` |

3. **Push to main branch**
   ```bash
   git add .
   git commit -m "Initial deployment setup"
   git push origin main
   ```

4. **Monitor deployment**
   - Go to Actions tab in your GitHub repository
   - Watch the deployment workflow execute
   - Check logs for any errors

## 🔄 Enabling the Data Pipeline

After deployment, the stored procedure and task are created but the task remains **SUSPENDED** for safety. To enable the automated data pipeline:

1. **Manually run the stored procedure once to test:**
   ```sql
   CALL CREATE_CUSTOMER_PROFILE_SP();
   ```

2. **Enable the scheduled task:**
   ```sql
   ALTER TASK CUSTOMER_PROFILE_TASK RESUME;
   ```

3. **Monitor task execution:**
   ```sql
   -- Check task status
   SHOW TASKS LIKE 'CUSTOMER_PROFILE_TASK';
   
   -- View task history
   SELECT * FROM V_TASK_HISTORY 
   WHERE NAME = 'CUSTOMER_PROFILE_TASK'
   ORDER BY SCHEDULED_TIME DESC;
   
   -- Check pipeline health
   SELECT * FROM PIPELINE_HEALTH ORDER BY TS DESC;
   ```

4. **View generated data:**
   ```sql
   -- Current profile data
   SELECT * FROM CUSTOMER_LINEITEM_PROFILE LIMIT 10;
   
   -- Timestamped snapshots
   SHOW TABLES LIKE 'CUSTOMER_LINEITEM_PROFILE_%';
   ```

**⚠️ Timezone Note**: Task schedules use UTC by default. You can specify named timezones like `Europe/Paris` in the cron expression, but history timestamps are always in UTC.

## 📊 SQL Files Overview

### 01_schema.sql
Creates the database, schema, and warehouse infrastructure needed for the dashboards.

### 02_tpch_views.sql
Defines views that join TPCH tables to provide enriched data:
- `V_CUSTOMER_DETAILS`: Customer information with region details
- `V_ORDER_DETAILS`: Order information with customer and region data
- `V_LINEITEM_DETAILS`: Line item details with product and supplier info
- `V_SUPPLIER_DETAILS`: Supplier information with nation and region

### 03_aggregations.sql
Creates aggregated views for dashboard KPIs:
- `V_MONTHLY_REVENUE_BY_REGION`: Monthly revenue trends by region
- `V_TOP_CUSTOMERS`: Customer ranking by revenue
- `V_PRODUCT_PERFORMANCE`: Product sales metrics
- `V_SUPPLIER_PERFORMANCE`: Supplier delivery and revenue metrics
- `V_ORDER_STATUS_SUMMARY`: Order status breakdown
- `V_MARKET_SEGMENT_ANALYSIS`: Market segment performance
- `V_SHIPPING_MODE_ANALYSIS`: Shipping method analysis

### 04_tasks.sql
Example task definitions for scheduled data refreshes (all commented out by default):
- Daily customer metrics refresh
- Hourly incremental updates
- Weekly reporting
- Task dependency chains

**Note**: Uncomment and modify tasks as needed for your use case.

### 05_grants.sql
Sets up role-based access control:
- `DASHBOARD_ANALYST_ROLE`: Read-only access to views
- `DASHBOARD_ENGINEER_ROLE`: Full management privileges
- Grants on database, schema, warehouse, and views
- Sample data access permissions

### 06_pipeline_prereqs.sql
Pipeline prerequisites and sample data access:
- Grants access to `SNOWFLAKE_SAMPLE_DATA.TPCH_SF1` schema
- Uses current database/schema from connection context
- Prepares environment for stored procedure execution

### 07_sp_customer_profile.sql
Python stored procedure using Snowpark-pandas:
- `CREATE_CUSTOMER_PROFILE_SP()`: Transforms TPCH line item and order data
- Filters out returned items (`L_RETURNFLAG != "A"`)
- Creates calculated fields: discount amount, price after discount, price per quantity
- Outputs both current table (`CUSTOMER_LINEITEM_PROFILE`) and timestamped snapshot
- Returns execution summary with row count

### 08_task_customer_profile.sql
Serverless task for automated execution:
- `CUSTOMER_PROFILE_TASK`: Calls the stored procedure hourly
- Created **SUSPENDED** by default for safety
- Uses UTC cron scheduling (`0 * * * * UTC`)
- Includes examples for timezone-specific scheduling

### 09_observability.sql
Pipeline monitoring and health checks:
- `PIPELINE_HEALTH`: Table for recording execution metrics
- `V_TASK_HISTORY`: View over Snowflake's task execution history
- Provides 7-day lookback for task monitoring

### 10_cleanup.sql
Demo cleanup and teardown:
- Suspends and drops the task safely
- Removes stored procedure and observability objects
- Includes commented commands for data cleanup
- Useful for development and testing cycles

## ⚙️ Advanced Usage

### Selective Execution

Execute only specific SQL files using environment variables or CLI flags:

```bash
# Using environment variable
ONLY=07_sp_customer_profile.sql python scripts/deploy.py

# Using CLI flag
python scripts/deploy.py --only 07_sp_customer_profile.sql

# Dry run to preview statements
DRY_RUN=1 python scripts/deploy.py
python scripts/deploy.py --dry-run

# Continue on errors (don't stop on first failure)
STOP_ON_ERROR=0 python scripts/deploy.py
```

### Environment Variable Controls

Set in `.env` file or environment:

- `DRY_RUN=1`: Print statements without executing
- `ONLY=filename.sql`: Execute only the specified file
- `STOP_ON_ERROR=0`: Continue execution even if statements fail

### Pipeline Management

```sql
-- Check what procedures exist
SHOW PROCEDURES LIKE 'CREATE_CUSTOMER_PROFILE%';

-- View task configuration
DESC TASK CUSTOMER_PROFILE_TASK;

-- Manual task execution (useful for testing)
EXECUTE TASK CUSTOMER_PROFILE_TASK;

-- Suspend task for maintenance
ALTER TASK CUSTOMER_PROFILE_TASK SUSPEND;

-- Change schedule (example: every 6 hours)
ALTER TASK CUSTOMER_PROFILE_TASK SET SCHEDULE = 'USING CRON 0 */6 * * * UTC';
```

## 🔒 Security Best Practices

1. **Never commit credentials**: Keep `.env` file in `.gitignore` (already configured)
2. **Use GitHub Secrets**: Store Snowflake credentials as encrypted secrets
3. **Principle of Least Privilege**: Use dedicated service account with minimal required permissions
4. **Key-Pair Authentication**: Consider switching from password to key-pair authentication for production
5. **Role Hierarchy**: Follow Snowflake's recommended role hierarchy
6. **Audit**: Regularly review access logs and granted privileges

## 🧪 Testing

To test the deployment locally without making changes:

```bash
# Dry run (add dry-run logic to deploy.py if needed)
python scripts/deploy.py
```

To verify deployed objects in Snowflake:

```sql
-- Check created views
SHOW VIEWS IN SCHEMA TPCH_DASHBOARDS.PUBLIC;

-- Test a view
SELECT * FROM TPCH_DASHBOARDS.PUBLIC.V_TOP_CUSTOMERS LIMIT 10;

-- Check roles and grants
SHOW GRANTS TO ROLE DASHBOARD_ANALYST_ROLE;
```

## 🔧 Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify your Snowflake account identifier format (e.g., `xy12345.eu-west-1`)
   - Check username and password in GitHub Secrets or `.env` file
   - Ensure the user has necessary privileges (SYSADMIN or higher recommended)

2. **Sample Data Not Available**
   - Verify `SNOWFLAKE_SAMPLE_DATA` database is accessible: `SHOW DATABASES LIKE 'SNOWFLAKE_SAMPLE_DATA';`
   - Contact your Snowflake administrator to enable sample data
   - Check grants: `SHOW GRANTS TO ROLE IDENTIFIER(CURRENT_ROLE());`

3. **Permission Denied for Pipeline Objects**
   - Ensure your user has `CREATE PROCEDURE`, `CREATE TASK` privileges
   - Check if you can access Python packages: stored procedures need package access
   - Verify warehouse permissions for task execution

4. **GitHub Actions Workflow Fails**
   - Verify all required secrets are configured (see secrets list above)
   - Check workflow logs for specific error messages
   - Ensure repository has Actions enabled and workflows can access secrets

5. **Task Not Running**
   - Verify task is RESUMED: `SHOW TASKS LIKE 'CUSTOMER_PROFILE_TASK';`
   - Check task history for errors: `SELECT * FROM V_TASK_HISTORY WHERE NAME = 'CUSTOMER_PROFILE_TASK';`
   - Ensure EXECUTE TASK privilege: `GRANT EXECUTE TASK ON ACCOUNT TO ROLE IDENTIFIER(CURRENT_ROLE());`
   - Verify serverless compute is available in your region

6. **Stored Procedure Fails**
   - Check Python package availability: ensure Snowpark-pandas is supported in your account
   - Verify sample data access before running the procedure
   - Test with smaller data sets first
   - Check Snowflake query history for detailed error messages

7. **Import Errors in Local Development**
   - Install requirements: `pip install -r requirements.txt`
   - Use virtual environment: `python -m venv .venv && source .venv/bin/activate`
   - Check Python version compatibility (3.8+ required, 3.11 recommended)

## 📈 Usage Examples

Once deployed, you can query the views for insights:

```sql
-- Top 10 customers by revenue
SELECT * FROM V_TOP_CUSTOMERS LIMIT 10;

-- Monthly revenue trend for 2024
SELECT * 
FROM V_MONTHLY_REVENUE_BY_REGION 
WHERE ORDER_MONTH >= '2024-01-01'
ORDER BY ORDER_MONTH;

-- Product performance analysis
SELECT * 
FROM V_PRODUCT_PERFORMANCE 
WHERE NET_REVENUE > 1000000
ORDER BY NET_REVENUE DESC;
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Test locally with your Snowflake account
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/your-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the terms specified in the LICENSE file.

## 📧 Support

For issues or questions:
- Open an issue in this repository
- Check Snowflake documentation: https://docs.snowflake.com/
- Review GitHub Actions documentation: https://docs.github.com/en/actions

## 🔄 Deployment Workflow

The deployment follows these steps:

1. **Trigger**: Push to `main` branch or manual workflow dispatch
2. **Checkout**: Code is checked out from the repository  
3. **Setup**: Python 3.11 environment is configured
4. **Install**: Dependencies are installed from `requirements.txt` (includes sqlparse for robust SQL parsing)
5. **Deploy**: Hardened `scripts/deploy.py` executes SQL files in lexicographic order:
   - 01_schema.sql (Database and schema setup)
   - 02_tpch_views.sql (TPCH detail views)
   - 03_aggregations.sql (KPI aggregations)
   - 04_tasks.sql (Example scheduled tasks)
   - 05_grants.sql (Security and RBAC)
   - 06_pipeline_prereqs.sql (Sample data grants)
   - 07_sp_customer_profile.sql (Snowpark-pandas stored procedure)
   - 08_task_customer_profile.sql (Serverless task - created SUSPENDED)
   - 09_observability.sql (Monitoring tables and views)
   - 10_cleanup.sql (Demo teardown script)
6. **Verify**: Deployment success with comprehensive logging and error handling

The deployment script now includes:
- Type hints and comprehensive error handling
- Robust SQL statement parsing with sqlparse  
- Support for dry-run, selective execution, and error handling modes
- Detailed logging of each statement execution

## ⚙️ Customization

### Adding New SQL Files

SQL files are executed in lexicographic order (01, 02, ..., 10, ...). To add new files:

1. Create a new file in `sql/` directory with appropriate numeric prefix (e.g., `11_custom_views.sql`)
2. Ensure the file works with the current database/schema context
3. Test locally with dry run: `python scripts/deploy.py --only 11_custom_views.sql --dry-run`
4. Test actual execution: `python scripts/deploy.py --only 11_custom_views.sql`
5. Commit and push to trigger automatic deployment

**Note**: Files 06-10 contain the new pipeline components. Add custom files with prefixes 11+ to maintain execution order.

### Modifying Aggregations

Edit `sql/03_aggregations.sql` to add or modify KPI views based on your requirements.

### Enabling Tasks

Uncomment task definitions in `sql/04_tasks.sql` and modify schedules as needed. Remember to resume tasks after creation:

```sql
ALTER TASK TASK_NAME RESUME;
```

---

**Built with ❄️ by the Snowflake community**

# Snowflake SQL Dashboards

Production-ready Snowflake TPCH dashboards with automated CI/CD deployment. This repository contains numbered SQL files for schema setup, KPI views, aggregations, scheduled tasks, and security grants, along with a Python deployment script and GitHub Actions workflow.

## 🚀 Features

- **Automated Deployment**: Python script runs SQL files in lexicographic order
- **TPCH Analytics**: Pre-built views and aggregations for Snowflake's sample TPCH data
- **CI/CD Integration**: GitHub Actions workflow for automatic deployment on push to main
- **Security Best Practices**: Role-based access control with granular permissions
- **Scheduled Tasks**: Example task definitions for data refresh workflows (commented)

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions deployment workflow
├── scripts/
│   └── deploy.py               # Python deployment script
├── sql/
│   ├── 01_schema.sql           # Database and schema setup
│   ├── 02_tpch_views.sql       # TPCH detail views
│   ├── 03_aggregations.sql     # KPI aggregations and metrics
│   ├── 04_tasks.sql            # Scheduled tasks (commented examples)
│   └── 05_grants.sql           # Security grants and RBAC
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
└── README.md                   # This file
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

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Snowflake credentials
   ```

4. **Update .env file with your Snowflake credentials**
   - `SNOW_ACCOUNT`: Your Snowflake account identifier (e.g., `xy12345.us-east-1`)
   - `SNOW_USER`: Your Snowflake username
   - `SNOW_PASSWORD`: Your Snowflake password
   - `SNOW_ROLE`: Role to use (e.g., `ACCOUNTADMIN` or `SYSADMIN`)
   - `SNOW_DATABASE`: Target database name (default: `TPCH_DASHBOARDS`)
   - `SNOW_SCHEMA`: Target schema name (default: `PUBLIC`)
   - `SNOW_WAREHOUSE`: Warehouse to use (default: `COMPUTE_WH`)

5. **Run the deployment script**
   ```bash
   python scripts/deploy.py
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

## 🔒 Security Best Practices

1. **Never commit credentials**: Keep `.env` file in `.gitignore`
2. **Use GitHub Secrets**: Store Snowflake credentials as encrypted secrets
3. **Principle of Least Privilege**: Use dedicated service account with minimal required permissions
4. **Role Hierarchy**: Follow Snowflake's recommended role hierarchy
5. **Audit**: Regularly review access logs and granted privileges

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
   - Verify your Snowflake account identifier format
   - Check username and password
   - Ensure the user has necessary privileges

2. **Sample Data Not Available**
   - Verify `SNOWFLAKE_SAMPLE_DATA` database is accessible
   - Contact your Snowflake administrator to enable sample data

3. **Permission Denied**
   - Ensure your user has `ACCOUNTADMIN` or `SYSADMIN` role
   - Check if you have CREATE DATABASE and CREATE ROLE privileges

4. **GitHub Actions Workflow Fails**
   - Verify all required secrets are configured
   - Check workflow logs for specific error messages
   - Ensure repository has Actions enabled

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
3. **Setup**: Python environment is configured
4. **Install**: Dependencies are installed from `requirements.txt`
5. **Deploy**: `scripts/deploy.py` executes SQL files in order:
   - 01_schema.sql
   - 02_tpch_views.sql
   - 03_aggregations.sql
   - 04_tasks.sql
   - 05_grants.sql
6. **Verify**: Deployment success or failure is reported

## ⚙️ Customization

### Adding New SQL Files

SQL files are executed in lexicographic order. To add new files:

1. Create a new file in `sql/` directory with a numeric prefix (e.g., `06_custom.sql`)
2. Ensure the file has proper USE DATABASE/SCHEMA statements
3. Test locally before committing
4. Push to trigger automatic deployment

### Modifying Aggregations

Edit `sql/03_aggregations.sql` to add or modify KPI views based on your requirements.

### Enabling Tasks

Uncomment task definitions in `sql/04_tasks.sql` and modify schedules as needed. Remember to resume tasks after creation:

```sql
ALTER TASK TASK_NAME RESUME;
```

---

**Built with ❄️ by the Snowflake community**

# 📊 BI Tools Connection Guide

Your enterprise Snowflake analytics platform is now ready for business intelligence tools! Here's how to connect each major BI platform.

## 🔗 Connection Parameters

**Use these connection details for all BI tools:**

```
Account: JHYWOUK-WA83239
Server: JHYWOUK-WA83239.snowflakecomputing.com
Username: ALGORYTHMOS
Database: TPCH_DASHBOARDS
Schema: PUBLIC
Warehouse: COMPUTE_WH
Role: DASHBOARD_ANALYST_ROLE (or DASHBOARD_ENGINEER_ROLE)
```

---

## 📈 Power BI Connection

### Method 1: Direct Connection
1. **Open Power BI Desktop**
2. **Get Data** → **More** → **Database** → **Snowflake**
3. **Enter Connection Details:**
   - Server: `JHYWOUK-WA83239.snowflakecomputing.com`
   - Warehouse: `COMPUTE_WH`
4. **Authentication:**
   - Username: `ALGORYTHMOS`
   - Password: [Your Snowflake password]
5. **Select Database:** `TPCH_DASHBOARDS`
6. **Select Tables/Views** from the navigator

### Method 2: ODBC Connection
1. Install **Snowflake ODBC Driver**
2. Configure ODBC Data Source:
   - Data Source Name: `Snowflake_Analytics`
   - Server: `JHYWOUK-WA83239.snowflakecomputing.com`
   - Database: `TPCH_DASHBOARDS`
   - Warehouse: `COMPUTE_WH`

### 🎯 Recommended Views for Power BI:
- `V_CUSTOMER_DETAILS` - Customer demographics and metrics
- `V_ORDER_DETAILS` - Order transactions and trends
- `V_MONTHLY_REVENUE_BY_REGION` - Geographic revenue analysis
- `V_MARKET_SEGMENT_ANALYSIS` - Market segmentation insights
- `CUSTOMER_LINEITEM_PROFILE` - Main fact table (4.5M+ records)

---

## 📊 Tableau Connection

### Method 1: Native Snowflake Connector
1. **Open Tableau Desktop**
2. **Connect** → **To a Server** → **Snowflake**
3. **Enter Connection Details:**
   - Server: `JHYWOUK-WA83239.snowflakecomputing.com`
   - Username: `ALGORYTHMOS`
   - Password: [Your Snowflake password]
4. **Advanced Options:**
   - Warehouse: `COMPUTE_WH`
   - Database: `TPCH_DASHBOARDS`
   - Schema: `PUBLIC`
   - Role: `DASHBOARD_ANALYST_ROLE`

### Method 2: Tableau Server/Online
1. Create **Published Data Source**
2. Use same connection parameters
3. Schedule **Extract Refresh** for optimal performance

### 🎯 Tableau Dashboard Ideas:
- **Executive Dashboard** - Revenue, orders, top customers
- **Geographic Analysis** - Regional performance mapping
- **Trend Analysis** - Time-series revenue and order patterns
- **Customer Segmentation** - Market segment performance

---

## 🔍 Looker Connection

### Database Connection Setup
1. **Admin Panel** → **Database** → **Connections**
2. **Add Connection:**
   - Database: `Snowflake`
   - Host: `JHYWOUK-WA83239.snowflakecomputing.com`
   - Database: `TPCH_DASHBOARDS`
   - Username: `ALGORYTHMOS`
   - Password: [Your Snowflake password]
3. **Additional Settings:**
   - Warehouse: `COMPUTE_WH`
   - Schema: `PUBLIC`
   - Role: `DASHBOARD_ANALYST_ROLE`

### LookML Model Creation
```lookml
connection: "snowflake_analytics"

include: "/views/*.view.lkml"

datagroup: analytics_default_datagroup {
  sql_trigger: SELECT MAX(updated_at) FROM CUSTOMER_LINEITEM_PROFILE;;
  max_cache_age: "1 hour"
}

explore: customer_lineitem_profile {
  type: table
  sql_table_name: PUBLIC.CUSTOMER_LINEITEM_PROFILE ;;
}
```

---

## 📋 Other BI Tools

### Grafana (For Real-time Monitoring)
- Install **Snowflake Data Source Plugin**
- Use same connection parameters
- Perfect for operational dashboards

### Metabase
1. **Admin** → **Databases** → **Add Database**
2. **Database Type:** Snowflake
3. Use standard connection parameters

### Apache Superset
```python
# Connection String
snowflake://ALGORYTHMOS:[password]@JHYWOUK-WA83239.snowflakecomputing.com/TPCH_DASHBOARDS?warehouse=COMPUTE_WH&role=DASHBOARD_ANALYST_ROLE
```

---

## 🔐 Security Best Practices

### 1. Use Dedicated Service Accounts
```sql
-- Create dedicated BI service users
CREATE USER POWERBI_USER PASSWORD='secure_password' 
DEFAULT_ROLE='DASHBOARD_ANALYST_ROLE';

CREATE USER TABLEAU_USER PASSWORD='secure_password' 
DEFAULT_ROLE='DASHBOARD_ANALYST_ROLE';
```

### 2. IP Restrictions (Optional)
```sql
-- Add network policies for BI tool IPs
CREATE NETWORK POLICY BI_TOOLS_POLICY
  ALLOWED_IP_LIST=('your.bi.server.ip/32');
```

### 3. Connection Pooling
- **Power BI:** Use DirectQuery for large datasets
- **Tableau:** Enable connection pooling in server settings
- **Looker:** Configure connection pool size

---

## 📊 Sample Queries for Testing

### Test Connection
```sql
SELECT COUNT(*) as total_records 
FROM CUSTOMER_LINEITEM_PROFILE;
-- Should return: 4,522,722
```

### Sample Dashboard Query
```sql
SELECT 
    N_NAME as region,
    SUM(PRICE_AFTER_DISCOUNT) as total_revenue,
    COUNT(DISTINCT O_CUSTKEY) as unique_customers,
    AVG(PRICE_PER_QTY) as avg_price_per_qty
FROM V_MONTHLY_REVENUE_BY_REGION
GROUP BY N_NAME
ORDER BY total_revenue DESC;
```

---

## 🚀 Performance Optimization

### 1. Use Analytical Views
- Pre-aggregated data in views like `V_MARKET_SEGMENT_ANALYSIS`
- Better performance than querying raw fact tables

### 2. Query Optimization
```sql
-- Use warehouse-specific sessions
ALTER SESSION SET WAREHOUSE = 'COMPUTE_WH';

-- Enable query caching
ALTER SESSION SET USE_CACHED_RESULT = TRUE;
```

### 3. Extract vs Live Connection
- **Large datasets (4.5M+ rows):** Use extracts/imports
- **Real-time needs:** Use live connections with views
- **Mixed approach:** Cache aggregations, live detail

---

## 🎯 Ready-to-Use Dashboard Templates

Your analytical views are perfectly structured for immediate dashboard creation:

1. **Executive Summary** → `V_CUSTOMER_DETAILS` + `V_ORDER_DETAILS`
2. **Sales Performance** → `V_MONTHLY_REVENUE_BY_REGION`
3. **Customer Analytics** → `V_MARKET_SEGMENT_ANALYSIS`
4. **Operational Metrics** → `CUSTOMER_LINEITEM_PROFILE` (main fact table)

**Your 4.5M+ record dataset is BI-ready!** 🎉
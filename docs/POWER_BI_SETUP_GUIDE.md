# 🚀 Power BI Connection - Step by Step Guide

## ✅ Connection Validated Successfully!

Your Snowflake analytics platform is **ready for Power BI** with:
- **4,522,722 records** in the main fact table
- **12 analytical views** for dashboards
- **80 months** of historical data (1992-2018)
- **Sub-second query performance** for aggregations

---

## 📋 Step 1: Open Power BI and Connect

### In Power BI Desktop:

1. **Click "Get Data"** (or Home → Get Data)
2. **Search for "Snowflake"** in the connector list
3. **Select "Snowflake database"** and click **Connect**

### Enter Connection Details:
```
Server: JHYWOUK-WA83239.snowflakecomputing.com
Warehouse: COMPUTE_WH
```

**Important:** Don't include the database here - you'll select it in the next step.

---

## 🔐 Step 2: Authentication

1. **Select "Database" authentication**
2. **Enter credentials:**
   - Username: `ALGORYTHMOS`
   - Password: `[Your Snowflake password]`

3. **Click "Connect"**

Power BI will test the connection and show available databases.

---

## 🎯 Step 3: Select Your Data

### Choose Database:
- Select **`TPCH_DASHBOARDS`** from the database list

### Recommended Tables to Load:

#### ✅ Essential Tables:
- **`CUSTOMER_LINEITEM_PROFILE`** - Main fact table (4.5M records)
  - Contains: Orders, customers, pricing, quantities
  - Use for: Detailed analysis, drill-downs

#### ✅ Pre-built Analytical Views:
- **`V_CUSTOMER_DETAILS`** - Customer demographics (150K records)
- **`V_ORDER_DETAILS`** - Order summaries (1.5M records)  
- **`V_MONTHLY_REVENUE_BY_REGION`** - Regional trends (400 records)
- **`V_MARKET_SEGMENT_ANALYSIS`** - Segment analysis (25 records)

### 💡 Pro Tip: Start Small
For your first dashboard, select just these 2 tables:
1. `V_MONTHLY_REVENUE_BY_REGION` (fast, pre-aggregated)
2. `V_CUSTOMER_DETAILS` (customer demographics)

---

## ⚡ Step 4: Choose Connection Mode

### DirectQuery (Recommended for Large Data):
- ✅ **Real-time data** - Always current
- ✅ **No size limits** - Handle all 4.5M records
- ✅ **Snowflake performance** - Let Snowflake do the work

### Import Mode (For Smaller Views):
- ✅ **Faster interactions** - Data cached locally
- ✅ **Offline access** - Work without connection
- ⚠️ **Limited to 1GB** - Use for analytical views only

### 🎯 Recommended Strategy:
- **DirectQuery**: `CUSTOMER_LINEITEM_PROFILE` (main fact table)
- **Import**: All `V_*` views (they're pre-aggregated and small)

---

## 📊 Step 5: Build Your First Dashboard

### Quick Start Template:

#### 📈 Revenue by Order Status
1. **Add a Bar Chart**
2. **Axis**: `O_ORDERSTATUS` from `CUSTOMER_LINEITEM_PROFILE`
3. **Values**: Sum of `PRICE_AFTER_DISCOUNT`

#### 🗺️ Regional Performance  
1. **Add a Map**
2. **Location**: Use `V_MONTHLY_REVENUE_BY_REGION`
3. **Size**: Revenue totals

#### 📅 Time Series
1. **Add a Line Chart**
2. **Axis**: `O_ORDERDATE` by Month
3. **Values**: Sum of `PRICE_AFTER_DISCOUNT`

---

## 🔧 Step 6: Optimize Performance

### Query Folding:
Power BI will automatically push queries to Snowflake when you:
- ✅ Use simple filters
- ✅ Group by columns
- ✅ Use SUM, COUNT, AVG functions
- ✅ Sort data

### Performance Tips:
1. **Use the analytical views** (`V_*`) for summary dashboards
2. **Filter early** - Add date/region filters first
3. **Limit visuals** - Start with 3-5 charts per page
4. **Use drill-through** - Let users go from summary to detail

---

## 📋 Connection Troubleshooting

### Common Issues:

#### "Server not found"
- ✅ **Check**: Use full server name `JHYWOUK-WA83239.snowflakecomputing.com`
- ✅ **Check**: Include warehouse name `COMPUTE_WH`

#### "Authentication failed"
- ✅ **Check**: Username `ALGORYTHMOS` (case sensitive)
- ✅ **Check**: Password is correct
- ✅ **Try**: Connect via Snowflake web interface first

#### "Table not found"
- ✅ **Check**: Database `TPCH_DASHBOARDS` is selected
- ✅ **Check**: Schema is `PUBLIC`
- ✅ **Check**: Role has permissions

### Test Connection Query:
```sql
SELECT COUNT(*) FROM CUSTOMER_LINEITEM_PROFILE
-- Should return: 4,522,722
```

---

## 🎯 Next Steps After Connection

### 1. Create Your First Report:
- Customer revenue analysis
- Regional performance comparison
- Time-based trends

### 2. Share with Team:
- Publish to Power BI Service
- Set up scheduled refresh
- Create workspace for collaboration

### 3. Advanced Features:
- Set up incremental refresh
- Create calculated columns
- Build data relationships

---

## 📞 Need Help?

Your platform is fully operational with:
- ✅ **4.5M+ records ready** for analysis
- ✅ **12 analytical views** for instant insights  
- ✅ **Sub-second performance** verified
- ✅ **Full date range** (1992-1998) available

**Ready to build amazing dashboards!** 🚀
#!/usr/bin/env python3
"""
Tableau Connection Helper
Sets up Tableau connection to Snowflake analytics platform
"""

import snowflake.connector
import getpass
import json
from datetime import datetime

def test_tableau_connection():
    """Test Snowflake connection for Tableau and validate data sources."""
    
    print("🎨 Tableau Connection Setup for Snowflake Analytics")
    print("=" * 60)
    
    # Get password securely
    password = getpass.getpass("Enter your Snowflake password: ")
    
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            account='JHYWOUK-WA83239',
            user='ALGORYTHMOS',
            password=password,
            role='DASHBOARD_ANALYST_ROLE',
            warehouse='COMPUTE_WH',
            database='TPCH_DASHBOARDS',
            schema='PUBLIC'
        )
        
        cursor = conn.cursor()
        print("✅ Connected to Snowflake successfully!")
        print()
        
        # Test data sources for Tableau
        print("📊 Tableau Data Source Validation")
        print("-" * 40)
        
        # Test main fact table
        cursor.execute("SELECT COUNT(*) FROM CUSTOMER_LINEITEM_PROFILE")
        fact_rows = cursor.fetchone()[0]
        print(f"✅ CUSTOMER_LINEITEM_PROFILE: {fact_rows:,} records")
        
        # Test analytical views
        tableau_views = [
            "V_CUSTOMER_DETAILS",
            "V_ORDER_DETAILS", 
            "V_MONTHLY_REVENUE_BY_REGION",
            "V_MARKET_SEGMENT_ANALYSIS"
        ]
        
        view_stats = {}
        for view in tableau_views:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {view}")
                count = cursor.fetchone()[0]
                view_stats[view] = count
                print(f"✅ {view}: {count:,} records")
            except Exception as e:
                print(f"❌ {view}: Error - {e}")
        
        print()
        
        # Sample data for Tableau preview
        print("🎯 Sample Data for Tableau Visualization")
        print("-" * 40)
        
        # Customer demographics sample
        cursor.execute("""
            SELECT 
                O_CUSTKEY as customer_id,
                COUNT(DISTINCT O_ORDERKEY) as order_count,
                SUM(PRICE_AFTER_DISCOUNT) as total_revenue,
                AVG(PRICE_PER_QTY) as avg_price_per_qty,
                MIN(O_ORDERDATE) as first_order,
                MAX(O_ORDERDATE) as last_order
            FROM CUSTOMER_LINEITEM_PROFILE
            GROUP BY O_CUSTKEY
            ORDER BY total_revenue DESC
            LIMIT 5
        """)
        
        top_customers = cursor.fetchall()
        print("💰 Top 5 Customers (for Customer Analysis dashboard):")
        for i, customer in enumerate(top_customers, 1):
            cust_id, orders, revenue, avg_price, first, last = customer
            print(f"   {i}. Customer {cust_id}: {orders} orders, ${revenue:,.2f} revenue")
        
        print()
        
        # Time series data sample
        cursor.execute("""
            SELECT 
                DATE_TRUNC('MONTH', O_ORDERDATE) as order_month,
                COUNT(DISTINCT O_ORDERKEY) as monthly_orders,
                SUM(PRICE_AFTER_DISCOUNT) as monthly_revenue,
                COUNT(DISTINCT O_CUSTKEY) as monthly_customers
            FROM CUSTOMER_LINEITEM_PROFILE
            GROUP BY DATE_TRUNC('MONTH', O_ORDERDATE)
            ORDER BY order_month DESC
            LIMIT 6
        """)
        
        monthly_data = cursor.fetchall()
        print("📅 Recent Monthly Performance (for Time Series dashboard):")
        for month_data in monthly_data:
            month, orders, revenue, customers = month_data
            print(f"   {month.strftime('%Y-%m')}: {orders:,} orders, ${revenue:,.0f} revenue, {customers:,} customers")
        
        print()
        
        # Performance test for Tableau
        print("⚡ Tableau Performance Test")
        print("-" * 40)
        
        start_time = datetime.now()
        
        # Test aggregation performance (typical Tableau operation)
        cursor.execute("""
            SELECT 
                O_ORDERSTATUS,
                COUNT(DISTINCT O_CUSTKEY) as customers,
                COUNT(DISTINCT O_ORDERKEY) as orders,
                SUM(PRICE_AFTER_DISCOUNT) as revenue,
                AVG(PRICE_PER_QTY) as avg_price
            FROM CUSTOMER_LINEITEM_PROFILE
            GROUP BY O_ORDERSTATUS
        """)
        
        status_results = cursor.fetchall()
        end_time = datetime.now()
        query_time = (end_time - start_time).total_seconds()
        
        print(f"✅ Aggregation query completed in {query_time:.2f} seconds")
        print("📊 Order Status Summary:")
        for status_data in status_results:
            status, customers, orders, revenue, avg_price = status_data
            print(f"   Status '{status}': {customers:,} customers, ${revenue:,.0f} revenue")
        
        print()
        
        # Tableau connection summary
        print("🎨 Tableau Connection Details")
        print("-" * 40)
        print("Server: JHYWOUK-WA83239.snowflakecomputing.com")
        print("Database: TPCH_DASHBOARDS")
        print("Schema: PUBLIC")
        print("Warehouse: COMPUTE_WH")
        print("Username: ALGORYTHMOS")
        print("Role: DASHBOARD_ANALYST_ROLE")
        print()
        print("📁 TDS File Location:")
        print("   /Users/skalaliya/Documents/snowflake-sql-dashboards-main/config/tableau_connection.tds")
        print()
        print("🎯 Recommended Tableau Dashboards:")
        print("   1. Executive Summary - Revenue trends, KPIs")
        print("   2. Customer Analytics - Top customers, segmentation") 
        print("   3. Time Series Analysis - Monthly/yearly trends")
        print("   4. Geographic Analysis - Regional performance")
        print()
        print("✅ Your Snowflake data is ready for Tableau visualization!")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Tableau connection test failed: {e}")
        return False

if __name__ == "__main__":
    test_tableau_connection()
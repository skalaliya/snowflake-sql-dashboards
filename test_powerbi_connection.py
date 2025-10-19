#!/usr/bin/env python3
"""
Power BI Connection Test Script
Tests connection to Snowflake and validates data for Power BI
"""

import snowflake.connector
import getpass
import json
from datetime import datetime

def test_powerbi_connection():
    """Test Snowflake connection and generate Power BI sample queries."""
    
    print("🔌 Power BI Connection Test for Snowflake Analytics")
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
        
        # Test 1: Basic connection and row count
        print("📊 Test 1: Data Availability Check")
        print("-" * 40)
        
        cursor.execute("SELECT COUNT(*) FROM CUSTOMER_LINEITEM_PROFILE")
        total_rows = cursor.fetchone()[0]
        print(f"✅ Main fact table: {total_rows:,} records available")
        
        cursor.execute("SHOW VIEWS")
        views = cursor.fetchall()
        analytical_views = [v for v in views if v[1].startswith('V_')]
        print(f"✅ Analytical views: {len(analytical_views)} views ready")
        print()
        
        # Test 2: Sample data for Power BI preview
        print("🔍 Test 2: Sample Data Preview (for Power BI)")
        print("-" * 40)
        
        sample_query = """
        SELECT 
            O_CUSTKEY,
            O_ORDERKEY,
            O_ORDERDATE,
            O_ORDERSTATUS,
            PRICE_AFTER_DISCOUNT,
            PRICE_PER_QTY,
            L_QUANTITY,
            L_EXTENDEDPRICE
        FROM CUSTOMER_LINEITEM_PROFILE 
        LIMIT 5
        """
        
        cursor.execute(sample_query)
        sample_data = cursor.fetchall()
        
        print("Sample records from main fact table:")
        for i, row in enumerate(sample_data, 1):
            cust_key, order_key, order_date, status, revenue, price_qty, quantity, extended_price = row
            print(f"  {i}. Customer {cust_key}: Order {order_key} - ${revenue:,.2f} revenue")
        print()
        
        # Test 3: Aggregated data performance
        print("⚡ Test 3: Aggregated Query Performance")
        print("-" * 40)
        
        start_time = datetime.now()
        
        perf_query = """
        SELECT 
            O_ORDERSTATUS as order_status,
            COUNT(DISTINCT O_CUSTKEY) as customers,
            COUNT(DISTINCT O_ORDERKEY) as orders,
            SUM(PRICE_AFTER_DISCOUNT) as total_revenue,
            AVG(PRICE_PER_QTY) as avg_price_per_qty,
            SUM(L_QUANTITY) as total_quantity
        FROM CUSTOMER_LINEITEM_PROFILE
        GROUP BY O_ORDERSTATUS
        ORDER BY total_revenue DESC
        """
        
        cursor.execute(perf_query)
        perf_results = cursor.fetchall()
        
        end_time = datetime.now()
        query_time = (end_time - start_time).total_seconds()
        
        print(f"✅ Query executed in {query_time:.2f} seconds")
        print("Performance by order status:")
        
        for i, row in enumerate(perf_results, 1):
            status, customers, orders, revenue, avg_price, quantity = row
            print(f"  {i}. Status '{status}': {customers:,} customers, ${revenue:,.2f} revenue")
        print()
        
        # Test 4: Date range validation
        print("📅 Test 4: Date Range Analysis")
        print("-" * 40)
        
        date_query = """
        SELECT 
            MIN(O_ORDERDATE) as earliest_date,
            MAX(O_ORDERDATE) as latest_date,
            COUNT(DISTINCT DATE_TRUNC('MONTH', O_ORDERDATE)) as months_of_data
        FROM CUSTOMER_LINEITEM_PROFILE
        """
        
        cursor.execute(date_query)
        date_result = cursor.fetchone()
        earliest, latest, months = date_result
        
        print(f"✅ Date range: {earliest} to {latest}")
        print(f"✅ Data spans: {months} months")
        print()
        
        # Test 5: View performance test
        print("👁️ Test 5: Analytical Views Performance")
        print("-" * 40)
        
        view_tests = [
            ("V_CUSTOMER_DETAILS", "Customer demographics"),
            ("V_ORDER_DETAILS", "Order transaction details"),
            ("V_MONTHLY_REVENUE_BY_REGION", "Regional revenue trends"),
            ("V_MARKET_SEGMENT_ANALYSIS", "Market segment analysis")
        ]
        
        for view_name, description in view_tests:
            try:
                start_time = datetime.now()
                cursor.execute(f"SELECT COUNT(*) FROM {view_name}")
                view_count = cursor.fetchone()[0]
                end_time = datetime.now()
                query_time = (end_time - start_time).total_seconds()
                
                print(f"✅ {view_name}: {view_count:,} records ({query_time:.2f}s)")
            except Exception as e:
                print(f"❌ {view_name}: Error - {e}")
        
        print()
        
        # Generate Power BI connection summary
        print("📋 Power BI Connection Summary")
        print("-" * 40)
        
        connection_info = {
            "server": "JHYWOUK-WA83239.snowflakecomputing.com",
            "database": "TPCH_DASHBOARDS",
            "schema": "PUBLIC",
            "warehouse": "COMPUTE_WH",
            "username": "ALGORYTHMOS",
            "role": "DASHBOARD_ANALYST_ROLE",
            "total_records": f"{total_rows:,}",
            "analytical_views": len(analytical_views),
            "date_range": f"{earliest} to {latest}",
            "months_of_data": months,
            "connection_test": "✅ PASSED"
        }
        
        print("Connection details for Power BI:")
        for key, value in connection_info.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        print()
        print("🎯 Power BI Setup Instructions:")
        print("1. Open Power BI Desktop")
        print("2. Get Data → More → Database → Snowflake")
        print("3. Enter server: JHYWOUK-WA83239.snowflakecomputing.com")
        print("4. Enter warehouse: COMPUTE_WH")
        print("5. Authenticate with your credentials")
        print("6. Select TPCH_DASHBOARDS database")
        print("7. Choose tables/views for your dashboard")
        print()
        print("🚀 Recommended starting tables:")
        print("   • CUSTOMER_LINEITEM_PROFILE (main fact table)")
        print("   • V_CUSTOMER_DETAILS (customer dimensions)")
        print("   • V_MONTHLY_REVENUE_BY_REGION (regional analysis)")
        print("   • V_MARKET_SEGMENT_ANALYSIS (segment analysis)")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    test_powerbi_connection()
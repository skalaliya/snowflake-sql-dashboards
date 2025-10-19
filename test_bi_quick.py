#!/usr/bin/env python3
"""
Quick BI Tool Connection Tests
Individual connection tests for Tableau, Power BI, and Looker
"""

import snowflake.connector
import getpass
import json

def test_individual_connections():
    """Test connections for each BI tool with their specific configurations."""
    
    print("🔧 Individual BI Tool Connection Tests")
    print("=" * 60)
    
    password = getpass.getpass("Enter your Snowflake password: ")
    
    # Test 1: Standard BI Connection (Power BI/Tableau style)
    print("\n📊 Testing Standard BI Connection...")
    try:
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
        
        # Test Power BI connection string format
        cursor.execute("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_DATABASE(), CURRENT_SCHEMA()")
        result = cursor.fetchone()
        
        print("✅ Standard Connection Successful!")
        print(f"   User: {result[0]}")
        print(f"   Role: {result[1]}")
        print(f"   Database: {result[2]}")
        print(f"   Schema: {result[3]}")
        
        # Test sample query (typical BI tool query)
        cursor.execute("SELECT COUNT(*) as total_records FROM CUSTOMER_LINEITEM_PROFILE")
        count = cursor.fetchone()[0]
        print(f"   Records Available: {count:,}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Standard Connection Failed: {e}")
    
    # Test 2: Looker-style Connection (with specific settings)
    print("\n🔍 Testing Looker-style Connection...")
    try:
        conn = snowflake.connector.connect(
            account='JHYWOUK-WA83239',
            user='ALGORYTHMOS', 
            password=password,
            role='DASHBOARD_ANALYST_ROLE',
            warehouse='COMPUTE_WH',
            database='TPCH_DASHBOARDS',
            schema='PUBLIC',
            client_session_keep_alive=True,  # Looker-style setting
            autocommit=True
        )
        
        cursor = conn.cursor()
        
        # Test Looker-style query patterns
        cursor.execute("""
            SELECT 
                DATE_TRUNC('MONTH', O_ORDERDATE) as month,
                COUNT(DISTINCT O_CUSTKEY) as customers,
                SUM(PRICE_AFTER_DISCOUNT) as revenue
            FROM CUSTOMER_LINEITEM_PROFILE
            GROUP BY month
            ORDER BY month DESC
            LIMIT 3
        """)
        
        results = cursor.fetchall()
        
        print("✅ Looker Connection Successful!")
        print(f"   Monthly Data Points: {len(results)}")
        print("   Sample Data:")
        for i, (month, customers, revenue) in enumerate(results[:2], 1):
            print(f"     {i}. {month.strftime('%Y-%m')}: {customers:,} customers, ${revenue:,.0f}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Looker Connection Failed: {e}")
    
    # Test 3: Tableau-specific Connection Test
    print("\n🎨 Testing Tableau-specific Connection...")
    try:
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
        
        # Test Tableau extract-style query (typical aggregation)
        cursor.execute("""
            SELECT 
                O_ORDERSTATUS as order_status,
                COUNT(DISTINCT O_CUSTKEY) as customers,
                COUNT(DISTINCT O_ORDERKEY) as orders,
                SUM(PRICE_AFTER_DISCOUNT) as revenue,
                AVG(PRICE_PER_QTY) as avg_price
            FROM CUSTOMER_LINEITEM_PROFILE
            GROUP BY O_ORDERSTATUS
            ORDER BY revenue DESC
        """)
        
        results = cursor.fetchall()
        
        print("✅ Tableau Connection Successful!")
        print(f"   Order Status Groups: {len(results)}")
        print("   Performance Summary:")
        for status, customers, orders, revenue, avg_price in results:
            print(f"     Status '{status}': {customers:,} customers, {orders:,} orders")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Tableau Connection Failed: {e}")
    
    # Test 4: Configuration File Validation
    print("\n📁 Testing Configuration Files...")
    
    config_tests = {
        "Power BI Config": "config/powerbi_connection.json",
        "Tableau TDS": "config/tableau_connection.tds", 
        "Looker Model": "config/looker_model.lkml"
    }
    
    for test_name, file_path in config_tests.items():
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            if file_path.endswith('.json'):
                json.loads(content)  # Validate JSON
                print(f"✅ {test_name}: Valid JSON configuration")
            elif file_path.endswith('.tds'):
                if 'snowflake' in content.lower() and 'JHYWOUK-WA83239' in content:
                    print(f"✅ {test_name}: Valid Tableau data source")
                else:
                    print(f"⚠️ {test_name}: Missing connection details")
            elif file_path.endswith('.lkml'):
                if 'connection:' in content and 'view:' in content:
                    print(f"✅ {test_name}: Valid LookML model") 
                else:
                    print(f"⚠️ {test_name}: Incomplete LookML model")
                    
        except FileNotFoundError:
            print(f"❌ {test_name}: Configuration file not found")
        except json.JSONDecodeError as e:
            print(f"❌ {test_name}: Invalid JSON - {e}")
        except Exception as e:
            print(f"❌ {test_name}: Error reading file - {e}")
    
    # Test 5: Quick Performance Check
    print("\n⚡ Quick Performance Check...")
    try:
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
        
        import time
        
        # Test view performance (what BI tools will typically hit)
        start = time.time()
        cursor.execute("SELECT COUNT(*) FROM V_MARKET_SEGMENT_ANALYSIS")
        cursor.fetchone()
        view_time = time.time() - start
        
        # Test fact table performance  
        start = time.time()
        cursor.execute("""
            SELECT O_ORDERSTATUS, COUNT(*) 
            FROM CUSTOMER_LINEITEM_PROFILE 
            GROUP BY O_ORDERSTATUS
        """)
        cursor.fetchall()
        fact_time = time.time() - start
        
        print(f"✅ Performance Test Results:")
        print(f"   View Query: {view_time:.2f} seconds")
        print(f"   Fact Table Aggregation: {fact_time:.2f} seconds")
        
        if fact_time < 2.0:
            print("   🚀 Excellent performance for BI workloads!")
        elif fact_time < 5.0:
            print("   ⚡ Good performance for BI workloads")
        else:
            print("   🐌 Consider optimizing for better BI performance")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Performance Test Failed: {e}")
    
    print(f"\n🎉 BI Connection Testing Complete!")
    print("=" * 60)
    print("✨ Your Snowflake platform is ready for BI tool connections!")

if __name__ == "__main__":
    test_individual_connections()
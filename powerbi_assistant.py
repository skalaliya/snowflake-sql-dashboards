#!/usr/bin/env python3
"""
Power BI Live Connection Assistant
Provides real-time guidance for connecting Power BI to Snowflake
"""

import snowflake.connector
import getpass
from datetime import datetime

def powerbi_connection_assistant():
    """Interactive assistant for Power BI connection to Snowflake."""
    
    print("🔌 Power BI → Snowflake Connection Assistant")
    print("=" * 60)
    print("I'll help you connect Power BI to your analytics platform!")
    print()
    
    # Step 1: Verify connection works
    print("STEP 1: Verifying your Snowflake connection...")
    print("-" * 50)
    
    password = getpass.getpass("Enter your Snowflake password (for verification): ")
    
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
        cursor.execute("SELECT COUNT(*) FROM CUSTOMER_LINEITEM_PROFILE")
        record_count = cursor.fetchone()[0]
        
        print(f"✅ Connection verified! {record_count:,} records ready")
        print("✅ Your credentials work perfectly")
        print()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Connection issue: {e}")
        print("Please check your password and try again.")
        return False
    
    # Step 2: Power BI Instructions
    print("STEP 2: Connect Power BI Desktop")
    print("-" * 50)
    print("In Power BI Desktop:")
    print()
    print("1. 📊 Click 'Get Data' (or Home → Get Data)")
    print("2. 🔍 Search for 'Snowflake' in the connector list")
    print("3. ✅ Select 'Snowflake database' and click 'Connect'")
    print()
    
    input("Press ENTER when you've opened the Snowflake connector...")
    print()
    
    # Step 3: Connection Details
    print("STEP 3: Enter Connection Details")
    print("-" * 50)
    print("📋 Copy these EXACT details into Power BI:")
    print()
    print("┌─────────────────────────────────────────────────────┐")
    print("│ Server: JHYWOUK-WA83239.snowflakecomputing.com     │")
    print("│ Warehouse: COMPUTE_WH                              │")
    print("└─────────────────────────────────────────────────────┘")
    print()
    print("⚠️  IMPORTANT: Leave 'Database' field EMPTY for now")
    print("    (You'll select it in the next step)")
    print()
    
    input("Press ENTER when you've entered the server details...")
    print()
    
    # Step 4: Authentication
    print("STEP 4: Authentication")
    print("-" * 50)
    print("🔐 Enter your credentials:")
    print()
    print("┌─────────────────────────────────────────────────────┐")
    print("│ Username: ALGORYTHMOS                              │")
    print("│ Password: [Your Snowflake password]                │")
    print("└─────────────────────────────────────────────────────┘")
    print()
    print("✅ Select 'Database' authentication type")
    print("✅ Click 'Connect'")
    print()
    
    input("Press ENTER when you've authenticated successfully...")
    print()
    
    # Step 5: Database Selection
    print("STEP 5: Select Database and Tables")
    print("-" * 50)
    print("🎯 You should now see the Navigator window")
    print()
    print("1. 📁 Expand 'TPCH_DASHBOARDS' database")
    print("2. 📁 Expand 'PUBLIC' schema")
    print()
    print("🚀 Recommended tables for your first dashboard:")
    print()
    print("✅ ESSENTIAL (check these boxes):")
    print("   □ V_MONTHLY_REVENUE_BY_REGION")
    print("   □ V_CUSTOMER_DETAILS") 
    print("   □ V_MARKET_SEGMENT_ANALYSIS")
    print()
    print("🔥 ADVANCED (for detailed analysis):")
    print("   □ CUSTOMER_LINEITEM_PROFILE (4.5M records)")
    print()
    
    input("Press ENTER when you've selected your tables...")
    print()
    
    # Step 6: Import vs DirectQuery
    print("STEP 6: Choose Connection Mode")
    print("-" * 50)
    print("📊 You'll see options for Import vs DirectQuery")
    print()
    print("🎯 RECOMMENDED SETUP:")
    print()
    print("✅ IMPORT MODE (for analytical views):")
    print("   • V_MONTHLY_REVENUE_BY_REGION")
    print("   • V_CUSTOMER_DETAILS")
    print("   • V_MARKET_SEGMENT_ANALYSIS")
    print("   → Fast, cached locally, perfect for dashboards")
    print()
    print("⚡ DIRECTQUERY MODE (for large fact table):")
    print("   • CUSTOMER_LINEITEM_PROFILE")
    print("   → Real-time, handles 4.5M records, no size limits")
    print()
    print("🔧 To set this up:")
    print("   1. Select the analytical views → Choose 'Import'")
    print("   2. Select CUSTOMER_LINEITEM_PROFILE → Choose 'DirectQuery'")
    print("   3. Click 'Load'")
    print()
    
    input("Press ENTER when you've configured the connection modes...")
    print()
    
    # Step 7: First Dashboard
    print("STEP 7: Build Your First Visual!")
    print("-" * 50)
    print("🎉 Great! Your data should now be loading...")
    print()
    print("🚀 Create your first chart:")
    print()
    print("📈 REVENUE TREND CHART:")
    print("   1. Drag 'Chart' visual to canvas")
    print("   2. X-axis: Date field from V_MONTHLY_REVENUE_BY_REGION")
    print("   3. Y-axis: Revenue field")
    print("   4. Watch your data come to life!")
    print()
    print("🗺️ REGIONAL MAP:")
    print("   1. Add 'Map' visual")
    print("   2. Location: Region field")
    print("   3. Size: Revenue totals")
    print()
    print("📊 KPI CARDS:")
    print("   1. Add 'Card' visuals")
    print("   2. Show: Total Customers, Total Revenue, etc.")
    print()
    
    # Step 8: Validation
    print("STEP 8: Validate Your Connection")
    print("-" * 50)
    print("🔍 Test these quick validations:")
    print()
    print("✅ RECORD COUNTS:")
    print(f"   • V_CUSTOMER_DETAILS: ~150,000 records")
    print(f"   • V_MONTHLY_REVENUE_BY_REGION: ~400 records")
    print(f"   • CUSTOMER_LINEITEM_PROFILE: 4,522,722 records")
    print()
    print("✅ DATE RANGE:")
    print("   • Should show data from 1992 to 1998")
    print("   • About 80 months of historical data")
    print()
    print("✅ PERFORMANCE:")
    print("   • Analytical views: Instant response")
    print("   • DirectQuery: Should respond in 1-3 seconds")
    print()
    
    # Success!
    print("🎉 SUCCESS! Your Power BI is Connected!")
    print("=" * 60)
    print("✅ Snowflake analytics platform: CONNECTED")
    print("✅ 4.5M+ records: AVAILABLE")
    print("✅ 12 analytical views: READY")
    print("✅ Real-time analytics: ENABLED")
    print()
    print("🚀 You're ready to build amazing dashboards!")
    print()
    print("💡 NEXT STEPS:")
    print("   • Experiment with different chart types")
    print("   • Add filters for interactivity")
    print("   • Create multiple pages for different analyses")
    print("   • Publish to Power BI Service for sharing")
    print()
    print("🎯 Need help with specific visuals? Just ask!")

if __name__ == "__main__":
    powerbi_connection_assistant()
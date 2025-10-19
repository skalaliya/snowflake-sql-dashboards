#!/usr/bin/env python3
"""
Test the deployed stored procedure by calling it directly.
"""

import snowflake.connector
from dotenv import load_dotenv
import os
import getpass

def test_stored_procedure():
    """Test the CREATE_CUSTOMER_PROFILE_SP stored procedure."""
    load_dotenv()
    
    account = os.getenv('SNOW_ACCOUNT', 'JHYWOUK-WA83239')
    user = os.getenv('SNOW_USER', 'ALGORYTHMOS')
    role = os.getenv('SNOW_ROLE', 'ACCOUNTADMIN')
    warehouse = os.getenv('SNOW_WAREHOUSE', 'COMPUTE_WH')
    database = os.getenv('SNOW_DATABASE', 'TPCH_DASHBOARDS')
    schema = os.getenv('SNOW_SCHEMA', 'PUBLIC')
    
    print("🧪 Testing Stored Procedure")
    print("=" * 50)
    
    # Get password securely
    password = getpass.getpass("Enter your Snowflake password: ")
    
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            account=account,
            user=user,
            password=password,
            role=role,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        
        cursor = conn.cursor()
        
        print(f"✅ Connected to {database}.{schema}")
        print(f"🏭 Using warehouse: {warehouse}")
        print()
        
        print("🚀 Executing CREATE_CUSTOMER_PROFILE_SP()...")
        cursor.execute("CALL CREATE_CUSTOMER_PROFILE_SP()")
        result = cursor.fetchone()
        
        print(f"✅ {result[0]}")
        print()
        
        print("🔍 Checking created tables...")
        
        # Check current profile table
        cursor.execute("SELECT COUNT(*) FROM CUSTOMER_LINEITEM_PROFILE")
        count = cursor.fetchone()[0]
        print(f"📊 CUSTOMER_LINEITEM_PROFILE: {count:,} rows")
        
        # Show sample data
        cursor.execute("SELECT * FROM CUSTOMER_LINEITEM_PROFILE LIMIT 5")
        sample_rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        print(f"📋 Sample data (first 5 rows):")
        print(f"   Columns: {', '.join(columns)}")
        for i, row in enumerate(sample_rows, 1):
            print(f"   Row {i}: {row}")
        
        # Check for timestamped tables
        cursor.execute("""
            SHOW TABLES LIKE 'CUSTOMER_LINEITEM_PROFILE_%'
        """)
        timestamped_tables = cursor.fetchall()
        
        if timestamped_tables:
            print(f"📅 Found {len(timestamped_tables)} timestamped snapshots:")
            for table_info in timestamped_tables:
                table_name = table_info[1]  # Table name is in the second column
                print(f"   - {table_name}")
        
        cursor.close()
        conn.close()
        
        print()
        print("🎉 Stored procedure test completed successfully!")
        print("💡 Your Snowflake data pipeline is fully operational!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_stored_procedure()
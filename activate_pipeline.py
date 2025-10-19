#!/usr/bin/env python3
"""
Activate the automated data pipeline - Resume the scheduled task and test execution
"""

import snowflake.connector
import getpass
import os
from dotenv import load_dotenv

def activate_pipeline():
    """Activate the customer profile pipeline."""
    load_dotenv()
    
    print("🚀 Activating Snowflake Data Pipeline")
    print("=" * 50)
    
    # Get password securely
    password = getpass.getpass("Enter your Snowflake password: ")
    
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            account='JHYWOUK-WA83239',
            user='ALGORYTHMOS',
            password=password,
            role='ACCOUNTADMIN',
            warehouse='COMPUTE_WH',
            database='TPCH_DASHBOARDS',
            schema='PUBLIC'
        )
        
        cursor = conn.cursor()
        
        print("✅ Connected to Snowflake")
        print()
        
        # Step 1: Check current task status
        print("🔍 Checking current task status...")
        cursor.execute("SHOW TASKS LIKE 'CUSTOMER_PROFILE_TASK'")
        task_info = cursor.fetchall()
        
        if task_info:
            task_name = task_info[0][1]
            current_state = task_info[0][7]
            print(f"📋 Task: {task_name}")
            print(f"📊 Current State: {current_state}")
            
            # Step 2: Resume the task if suspended
            if current_state == 'SUSPENDED':
                print("\n🔄 Resuming automated task...")
                cursor.execute("ALTER TASK CUSTOMER_PROFILE_TASK RESUME")
                print("✅ Task resumed! Pipeline is now automated.")
            else:
                print(f"✅ Task is already in {current_state} state")
        
        print()
        
        # Step 3: Manual execution test
        print("🧪 Testing manual execution...")
        cursor.execute("CALL CREATE_CUSTOMER_PROFILE_SP()")
        result = cursor.fetchone()
        print(f"✅ Manual execution result: {result[0]}")
        
        print()
        
        # Step 4: Check pipeline health
        print("💊 Checking pipeline health...")
        cursor.execute("SELECT COUNT(*) FROM CUSTOMER_LINEITEM_PROFILE")
        current_rows = cursor.fetchone()[0]
        print(f"📊 Current profile records: {current_rows:,}")
        
        # Check for timestamped snapshots
        cursor.execute("SHOW TABLES LIKE 'CUSTOMER_LINEITEM_PROFILE_%'")
        snapshots = cursor.fetchall()
        print(f"📸 Historical snapshots: {len(snapshots)}")
        
        print()
        
        # Step 5: Show task schedule info
        print("⏰ Pipeline Schedule Information:")
        cursor.execute("""
            SELECT 
                TASK_NAME,
                STATE,
                SCHEDULE,
                NEXT_SCHEDULED_TIME
            FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
                TASK_NAME => 'CUSTOMER_PROFILE_TASK'
            )) 
            ORDER BY SCHEDULED_TIME DESC 
            LIMIT 1
        """)
        
        schedule_info = cursor.fetchall()
        if schedule_info:
            for info in schedule_info:
                print(f"   📅 Task: {info[0]}")
                print(f"   🔄 State: {info[1]}")
                print(f"   ⏰ Schedule: {info[2] or 'Manual trigger only'}")
                print(f"   ⏭️  Next Run: {info[3] or 'Manual trigger only'}")
        
        print()
        print("🎉 Pipeline Activation Complete!")
        print("💡 Your data pipeline is now fully operational and automated!")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Activation failed: {e}")
        return False

if __name__ == "__main__":
    activate_pipeline()
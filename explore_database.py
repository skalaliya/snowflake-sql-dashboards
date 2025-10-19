#!/usr/bin/env python3
"""
Quick database explorer to show all objects in TPCH_DASHBOARDS
"""

import snowflake.connector
import getpass
import os
from dotenv import load_dotenv

def explore_database():
    load_dotenv()
    
    password = getpass.getpass("Enter your Snowflake password: ")
    
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
    
    print("🏢 TPCH_DASHBOARDS Database Explorer")
    print("=" * 60)
    print(f"📍 Location: JHYWOUK-WA83239.snowflakecomputing.com")
    print(f"🗃️  Database: TPCH_DASHBOARDS")
    print(f"📁 Schema: PUBLIC")
    print(f"🏭 Warehouse: ANALYTICS_WH")
    print()
    
    # Show database size and object counts
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'PUBLIC'")
    table_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.VIEWS WHERE TABLE_SCHEMA = 'PUBLIC'")
    view_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.PROCEDURES WHERE PROCEDURE_SCHEMA = 'PUBLIC'")
    proc_count = cursor.fetchone()[0]
    
    print("📊 Object Summary:")
    print(f"   Tables: {table_count}")
    print(f"   Views: {view_count}")
    print(f"   Procedures: {proc_count}")
    print()
    
    # Show tables with row counts
    print("📋 Tables:")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[1]
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            print(f"   📊 {table_name}: {row_count:,} rows")
        except:
            print(f"   📊 {table_name}: (unable to count)")
    
    print()
    
    # Show views
    print("👁️  Views:")
    cursor.execute("SHOW VIEWS")
    views = cursor.fetchall()
    for view in views:
        view_name = view[1]
        print(f"   📈 {view_name}")
    
    print()
    
    # Show procedures
    print("🐍 Stored Procedures:")
    cursor.execute("SHOW PROCEDURES")
    procedures = cursor.fetchall()
    for proc in procedures:
        proc_name = proc[1]
        language = proc[6] if len(proc) > 6 else "SQL"
        print(f"   ⚙️  {proc_name} ({language})")
    
    print()
    
    # Show tasks
    print("⏰ Scheduled Tasks:")
    cursor.execute("SHOW TASKS")
    tasks = cursor.fetchall()
    for task in tasks:
        task_name = task[1]
        state = task[7] if len(task) > 7 else "Unknown"
        print(f"   🕐 {task_name} (Status: {state})")
    
    print()
    print("💡 Access Methods:")
    print(f"   🌐 Web UI: https://app.snowflake.com/")
    print(f"   🔗 Direct URL: https://app.snowflake.com/JHYWOUK-WA83239/#/data/databases/TPCH_DASHBOARDS")
    print(f"   💻 SQL: USE DATABASE TPCH_DASHBOARDS; USE SCHEMA PUBLIC;")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    explore_database()
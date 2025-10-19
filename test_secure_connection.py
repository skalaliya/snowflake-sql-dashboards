#!/usr/bin/env python3
"""
Secure Snowflake Connection Tester
Prompts for password securely without storing it in files.
"""

import getpass
import snowflake.connector
from dotenv import load_dotenv
import os
import sys

def test_secure_connection():
    """Test Snowflake connection with secure password input."""
    load_dotenv()
    
    account = os.getenv('SNOW_ACCOUNT', 'JHYWOUK-WA83239')
    user = os.getenv('SNOW_USER', 'ALGORYTHMOS')
    role = os.getenv('SNOW_ROLE', 'ACCOUNTADMIN')
    warehouse = os.getenv('SNOW_WAREHOUSE', 'COMPUTE_WH')
    
    print("🔐 Secure Snowflake Connection Test")
    print("=" * 50)
    print(f"Account: {account}")
    print(f"User: {user}")
    print(f"Role: {role}")
    print(f"Warehouse: {warehouse}")
    print()
    
    # Securely prompt for password
    try:
        password = getpass.getpass("Enter your Snowflake password: ")
        
        if not password.strip():
            print("❌ Password cannot be empty")
            return False
            
        print("\n🔄 Attempting connection...")
        
        # Test connection
        conn = snowflake.connector.connect(
            account=account,
            user=user,
            password=password,
            role=role,
            warehouse=warehouse
        )
        
        # Test basic query
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_ACCOUNT(), CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()")
        result = cursor.fetchone()
        
        print("✅ CONNECTION SUCCESSFUL!")
        print(f"   Account: {result[0]}")
        print(f"   User: {result[1]}")
        print(f"   Role: {result[2]}")
        print(f"   Warehouse: {result[3]}")
        
        # Test access to sample data
        print("\n🔍 Testing access to SNOWFLAKE_SAMPLE_DATA...")
        try:
            cursor.execute("SELECT COUNT(*) FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER LIMIT 1")
            count_result = cursor.fetchone()
            print(f"✅ Sample data accessible - Customer table has {count_result[0]:,} rows")
        except Exception as e:
            print(f"⚠️  Sample data access issue: {e}")
            print("   This won't prevent basic deployment but may affect the pipeline")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Ready to deploy! Your connection works perfectly.")
        print("\nNext steps:")
        print("1. Update your .env file with the password")
        print("2. Run: uv run python scripts/deploy.py --only 01_schema.sql")
        print("3. If successful, run full deployment: uv run python scripts/deploy.py")
        
        return True
        
    except KeyboardInterrupt:
        print("\n❌ Connection test cancelled by user")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        
        if "Incorrect username or password" in str(e):
            print("- Check your username and password")
            print("- Verify account is not locked")
        elif "SAML" in str(e):
            print("- Your account may require SSO authentication")
            print("- Try logging in through web browser first")
        elif "404" in str(e):
            print("- Account identifier may be incorrect")
            print("- Check Snowflake web UI for correct account ID")
        else:
            print(f"- Unexpected error: {e}")
            
        return False

if __name__ == "__main__":
    success = test_secure_connection()
    sys.exit(0 if success else 1)
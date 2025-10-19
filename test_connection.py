#!/usr/bin/env python3
"""
Simple Snowflake connection test script.
Tests different account formats and authentication methods.
"""

import snowflake.connector
from dotenv import load_dotenv
import os
import sys

load_dotenv()

def test_connection(account, user, auth_method, role=None, password=None):
    """Test a single connection configuration."""
    try:
        conn_params = {
            'account': account,
            'user': user,
            'authenticator': auth_method
        }
        
        if password and auth_method != 'externalbrowser':
            conn_params['password'] = password
        if role:
            conn_params['role'] = role
            
        print(f"  Connecting with: account={account}, auth={auth_method}")
        
        conn = snowflake.connector.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_ACCOUNT(), CURRENT_USER(), CURRENT_ROLE()")
        result = cursor.fetchone()
        print(f"  ✅ SUCCESS! Account: {result[0]}, User: {result[1]}, Role: {result[2]}")
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Failed: {str(e)}")
        return False

def main():
    # Test different account formats
    account_formats = [
        "JHYWOUK-WA83239",
        "jhywouk-wa83239"
    ]

    user = os.getenv('SNOW_USER', 'ALGORYTHMOS')
    password = os.getenv('SNOW_PASSWORD', '')
    role = os.getenv('SNOW_ROLE', 'ACCOUNTADMIN')

    print("Testing Snowflake connection configurations...")
    print(f"User: {user}")
    print(f"Role: {role}")
    print("=" * 60)

    # Test each account format with external browser auth
    for account in account_formats:
        print(f"\n🔍 Testing account: {account}")
        
        if test_connection(account, user, 'externalbrowser', role):
            print(f"\n✅ SUCCESS! Use account identifier: {account}")
            return account
            
    # If external browser fails, try password auth if available
    if password:
        print(f"\n🔍 Trying password authentication...")
        for account in account_formats:
            print(f"\nTesting account: {account} (password auth)")
            if test_connection(account, user, 'snowflake', role, password):
                print(f"\n✅ SUCCESS! Use account identifier: {account}")
                return account
    
    print("\n❌ All connection attempts failed")
    print("\nTroubleshooting suggestions:")
    print("1. Verify your Snowflake URL - what do you use to login?")
    print("2. Check if your account uses SSO (Okta, Azure AD, etc.)")
    print("3. Try logging into Snowflake web UI first")
    print("4. Your account identifier might be different")
    print("   - Check Snowflake web UI → Admin → Accounts")
    print("   - Look for 'Account Identifier' or 'Account Locator'")
    return None

if __name__ == "__main__":
    main()
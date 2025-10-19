#!/usr/bin/env python3
"""
Debug script to check GitHub Actions environment and secrets
"""
import os
import sys

def debug_environment():
    """Debug GitHub Actions environment and secrets."""
    print("🔍 GitHub Actions Environment Debug")
    print("=" * 50)
    
    # Check all required environment variables
    required_vars = [
        'SNOW_ACCOUNT',
        'SNOW_USER', 
        'SNOW_PASSWORD',
        'SNOW_ROLE',
        'SNOW_WAREHOUSE',
        'SNOW_DATABASE',
        'SNOW_SCHEMA'
    ]
    
    print("📋 Checking required environment variables:")
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask password for security
            display_value = "***" if "PASSWORD" in var else value
            print(f"   ✅ {var} = {display_value}")
        else:
            print(f"   ❌ {var} = NOT SET")
            missing_vars.append(var)
    
    print()
    
    if missing_vars:
        print(f"❌ Missing {len(missing_vars)} required variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print()
        print("💡 Please add these as GitHub repository secrets:")
        print("   Settings → Secrets and variables → Actions → New repository secret")
        return False
    else:
        print("✅ All required environment variables are set!")
        
        # Test basic imports
        print("\n🧪 Testing Python imports...")
        try:
            import snowflake.connector
            print("   ✅ snowflake.connector imported successfully")
        except ImportError as e:
            print(f"   ❌ Failed to import snowflake.connector: {e}")
            return False
            
        try:
            from dotenv import load_dotenv
            print("   ✅ dotenv imported successfully")
        except ImportError as e:
            print(f"   ❌ Failed to import dotenv: {e}")
            return False
            
        # Test connection (without actually connecting to avoid overuse)
        print("\n🔗 Connection parameters look valid!")
        print("   Ready for Snowflake deployment")
        return True

if __name__ == "__main__":
    success = debug_environment()
    if not success:
        print("\n🚨 Environment check failed!")
        sys.exit(1)
    else:
        print("\n🎉 Environment check passed!")
        print("   Proceeding with deployment...")
        sys.exit(0)
#!/usr/bin/env python3
"""
BI Connection String Generator
Generates ready-to-use connection strings and configurations for all BI tools
"""

def generate_connection_strings():
    """Generate connection strings for different BI tools."""
    
    print("🔗 BI Tool Connection String Generator")
    print("=" * 60)
    
    # Base connection parameters
    connection_params = {
        'server': 'JHYWOUK-WA83239.snowflakecomputing.com',
        'account': 'JHYWOUK-WA83239',
        'database': 'TPCH_DASHBOARDS',
        'schema': 'PUBLIC',
        'warehouse': 'COMPUTE_WH',
        'username': 'ALGORYTHMOS',
        'role': 'DASHBOARD_ANALYST_ROLE'
    }
    
    print("📋 Universal Connection Parameters")
    print("-" * 40)
    for key, value in connection_params.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    print("\n🎨 Tableau Connection")
    print("-" * 40)
    print("Method 1: Import TDS File")
    print("   File: config/tableau_connection.tds")
    print("   Action: Connect → To a File → Select TDS file")
    print()
    print("Method 2: Manual Connection")
    print(f"   Server: {connection_params['server']}")
    print(f"   Username: {connection_params['username']}")
    print("   Password: [Your Snowflake Password]")
    print(f"   Warehouse: {connection_params['warehouse']}")
    print(f"   Database: {connection_params['database']}")
    print(f"   Role: {connection_params['role']}")
    
    print("\n📊 Power BI Connection")
    print("-" * 40)
    print("Get Data → More → Snowflake")
    print(f"   Server: {connection_params['server']}")
    print(f"   Warehouse: {connection_params['warehouse']}")
    print("   Authentication: Database")
    print(f"   Username: {connection_params['username']}")
    print("   Password: [Your Snowflake Password]")
    print(f"   Database: {connection_params['database']}")
    
    print("\n🔍 Looker Studio Connection")
    print("-" * 40)
    print("Create → Data Source → Snowflake")
    print(f"   Server: {connection_params['server']}")
    print(f"   Database: {connection_params['database']}")
    print(f"   Schema: {connection_params['schema']}")
    print(f"   Warehouse: {connection_params['warehouse']}")
    print(f"   Username: {connection_params['username']}")
    print("   Password: [Your Snowflake Password]")
    print(f"   Role: {connection_params['role']}")
    
    print("\n🔍 Looker Cloud Connection")
    print("-" * 40)
    print("Admin → Database → Connections → New")
    print("   Dialect: Snowflake")
    print(f"   Host: {connection_params['server']}")
    print(f"   Database: {connection_params['database']}")
    print(f"   Username: {connection_params['username']}")
    print("   Password: [Your Snowflake Password]")
    print(f"   Warehouse: {connection_params['warehouse']}")
    print(f"   Role: {connection_params['role']}")
    print("   Additional JDBC: CLIENT_SESSION_KEEP_ALIVE=true")
    
    print("\n🔌 JDBC Connection String")
    print("-" * 40)
    jdbc_url = f"jdbc:snowflake://{connection_params['server']}/?warehouse={connection_params['warehouse']}&db={connection_params['database']}&schema={connection_params['schema']}&role={connection_params['role']}"
    print(f"   URL: {jdbc_url}")
    print(f"   Username: {connection_params['username']}")
    print("   Password: [Your Snowflake Password]")
    
    print("\n🔌 ODBC Connection String")  
    print("-" * 40)
    odbc_string = f"Driver=SnowflakeDSIIDriver;Server={connection_params['server']};Database={connection_params['database']};Schema={connection_params['schema']};Warehouse={connection_params['warehouse']};Role={connection_params['role']};UID={connection_params['username']};PWD=[Your Password]"
    print(f"   Connection String:")
    print(f"   {odbc_string}")
    
    print("\n🐍 Python Connection (Snowflake Connector)")
    print("-" * 40)
    print("   import snowflake.connector")
    print("   conn = snowflake.connector.connect(")
    print(f"       account='{connection_params['account']}',")
    print(f"       user='{connection_params['username']}',")
    print("       password='[Your Password]',")
    print(f"       role='{connection_params['role']}',")
    print(f"       warehouse='{connection_params['warehouse']}',") 
    print(f"       database='{connection_params['database']}',")
    print(f"       schema='{connection_params['schema']}'")
    print("   )")
    
    print("\n📊 Available Data Sources")
    print("-" * 40)
    data_sources = [
        ("CUSTOMER_LINEITEM_PROFILE", "4.5M records", "Main fact table - orders, customers, pricing"),
        ("V_CUSTOMER_DETAILS", "150K records", "Customer demographics and info"),
        ("V_ORDER_DETAILS", "1.5M records", "Order summaries and metrics"),
        ("V_MONTHLY_REVENUE_BY_REGION", "400 records", "Regional performance over time"),
        ("V_MARKET_SEGMENT_ANALYSIS", "25 records", "Market segment analysis"),
    ]
    
    for table, size, description in data_sources:
        print(f"   ✅ {table}")
        print(f"      Size: {size}")
        print(f"      Use: {description}")
        print()
    
    print("🚀 Quick Start Tips")
    print("-" * 40)
    print("   1. Start with V_MARKET_SEGMENT_ANALYSIS (small, fast)")
    print("   2. Use V_MONTHLY_REVENUE_BY_REGION for time series")
    print("   3. Connect to CUSTOMER_LINEITEM_PROFILE for detailed analysis")
    print("   4. Use DirectQuery/Live connection for real-time data")
    print("   5. Import smaller views for faster dashboard interactions")
    
    print("\n✨ Your connections are ready! Choose your BI tool and connect! ✨")

if __name__ == "__main__":
    generate_connection_strings()
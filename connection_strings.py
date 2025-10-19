#!/usr/bin/env python3
"""
BI Connection String Generator
Generates ready-to-copy connection strings for all BI tools
"""

def generate_connection_strings():
    """Generate connection strings for all BI tools"""
    
    print("📋 BI TOOLS CONNECTION STRINGS")
    print("=" * 80)
    print("Copy and paste these into your BI tools for instant connection:")
    print()
    
    # Tableau Connection
    print("🎨 TABLEAU DESKTOP/SERVER")
    print("-" * 40)
    print("Method 1 - Import TDS File:")
    print("   File: config/tableau_connection.tds")
    print("   Action: Connect → To a File → Select TDS file")
    print()
    print("Method 2 - Manual Connection:")
    print("   Server: JHYWOUK-WA83239.snowflakecomputing.com")
    print("   Username: ALGORYTHMOS")
    print("   Password: [Your Snowflake Password]")
    print("   Warehouse: COMPUTE_WH")
    print("   Database: TPCH_DASHBOARDS")
    print("   Schema: PUBLIC")
    print("   Role: DASHBOARD_ANALYST_ROLE")
    print()
    
    # Power BI Connection
    print("📊 POWER BI DESKTOP/SERVICE")
    print("-" * 40)
    print("Connection Steps:")
    print("   1. Get Data → More → Database → Snowflake")
    print("   2. Server: JHYWOUK-WA83239.snowflakecomputing.com")
    print("   3. Warehouse: COMPUTE_WH")
    print("   4. Authentication: Database")
    print("   5. Username: ALGORYTHMOS")
    print("   6. Password: [Your Snowflake Password]")
    print("   7. Database: TPCH_DASHBOARDS")
    print("   8. Schema: PUBLIC")
    print()
    
    # Looker Studio Connection
    print("🔍 LOOKER STUDIO (FREE)")
    print("-" * 40)
    print("Connection Details:")
    print("   Connector: Snowflake (or Partner Connector)")
    print("   Server: JHYWOUK-WA83239.snowflakecomputing.com")
    print("   Warehouse: COMPUTE_WH")
    print("   Database: TPCH_DASHBOARDS")
    print("   Schema: PUBLIC")
    print("   Username: ALGORYTHMOS")
    print("   Password: [Your Snowflake Password]")
    print("   Role: DASHBOARD_ANALYST_ROLE")
    print()
    
    # Looker Cloud Connection  
    print("🔍 LOOKER CLOUD (PAID)")
    print("-" * 40)
    print("Database Connection:")
    print("   Dialect: Snowflake")
    print("   Host: JHYWOUK-WA83239.snowflakecomputing.com")
    print("   Database: TPCH_DASHBOARDS")
    print("   Schema: PUBLIC")
    print("   Username: LOOKER_USER (or ALGORYTHMOS)")
    print("   Password: [Your Snowflake Password]")
    print("   Warehouse: COMPUTE_WH")
    print("   Role: LOOKER_ROLE (or DASHBOARD_ANALYST_ROLE)")
    print("   LookML Model: config/looker_model.lkml")
    print()
    
    # JDBC/ODBC Connection
    print("🔗 JDBC/ODBC CONNECTION (ANY BI TOOL)")
    print("-" * 40)
    print("JDBC URL:")
    jdbc_url = "jdbc:snowflake://JHYWOUK-WA83239.snowflakecomputing.com/?warehouse=COMPUTE_WH&db=TPCH_DASHBOARDS&schema=PUBLIC&role=DASHBOARD_ANALYST_ROLE"
    print(f"   {jdbc_url}")
    print()
    print("ODBC Connection String:")
    odbc_str = "Driver={SnowflakeDSIIDriver};Server=JHYWOUK-WA83239.snowflakecomputing.com;Database=TPCH_DASHBOARDS;Schema=PUBLIC;Warehouse=COMPUTE_WH;Role=DASHBOARD_ANALYST_ROLE"
    print(f"   {odbc_str}")
    print("   Username: ALGORYTHMOS")
    print("   Password: [Your Snowflake Password]")
    print()
    
    # Data Sources Summary
    print("📊 AVAILABLE DATA SOURCES")
    print("-" * 40)
    print("Main Tables:")
    print("   ✅ CUSTOMER_LINEITEM_PROFILE (4.5M records) - Main fact table")
    print()
    print("Analytical Views:")
    print("   ✅ V_CUSTOMER_DETAILS (150K records) - Customer demographics")
    print("   ✅ V_ORDER_DETAILS (1.5M records) - Order summaries")
    print("   ✅ V_MONTHLY_REVENUE_BY_REGION (400 records) - Regional trends")
    print("   ✅ V_MARKET_SEGMENT_ANALYSIS (25 records) - Market segments") 
    print("   ✅ V_SUPPLIER_PERFORMANCE (10K records) - Supplier metrics")
    print("   ✅ Plus 7 more analytical views available")
    print()
    
    # Sample Queries
    print("💡 SAMPLE QUERIES FOR TESTING")
    print("-" * 40)
    print("Test Connection:")
    print("   SELECT COUNT(*) FROM CUSTOMER_LINEITEM_PROFILE;")
    print()
    print("Executive KPIs:")
    print("   SELECT")
    print("       COUNT(DISTINCT O_CUSTKEY) as customers,")
    print("       COUNT(DISTINCT O_ORDERKEY) as orders,")
    print("       SUM(PRICE_AFTER_DISCOUNT) as revenue")
    print("   FROM CUSTOMER_LINEITEM_PROFILE;")
    print()
    print("Monthly Revenue Trend:")
    print("   SELECT")
    print("       DATE_TRUNC('MONTH', O_ORDERDATE) as month,")
    print("       SUM(PRICE_AFTER_DISCOUNT) as revenue")
    print("   FROM CUSTOMER_LINEITEM_PROFILE")
    print("   GROUP BY month")
    print("   ORDER BY month;")
    print()
    
    # Security Notes
    print("🔐 SECURITY NOTES")
    print("-" * 40)
    print("✅ All connections use SSL/TLS encryption")
    print("✅ Role-based access control (RBAC) implemented")
    print("✅ Read-only permissions for BI tools")
    print("✅ Dedicated service users available (see sql/bi_security_setup.sql)")
    print("✅ Network policies configurable for production")
    print()
    
    # Performance Tips
    print("⚡ PERFORMANCE TIPS")
    print("-" * 40)
    print("✅ Use analytical views (V_*) for faster aggregations")
    print("✅ Apply date filters early in queries")
    print("✅ Use DirectQuery for large datasets (Power BI)")
    print("✅ Enable connection pooling where available")
    print("✅ Cache frequently used aggregations")
    print()
    
    print("🎯 YOUR ENTERPRISE BI PLATFORM IS READY!")
    print("=" * 80)
    print("📈 6M+ records | ⚡ Sub-second performance | 🔐 Enterprise security")
    print("🚀 Connect any BI tool and start building amazing dashboards! 🚀")

if __name__ == "__main__":
    generate_connection_strings()
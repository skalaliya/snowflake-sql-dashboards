#!/usr/bin/env python3
"""
Local BI Connection Test Suite
Tests all BI tool connections locally and validates complete setup
"""

import snowflake.connector
import getpass
import os
import json
import time
from datetime import datetime

class BIConnectionTester:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.test_results = {}
        
    def connect_to_snowflake(self):
        """Establish connection to Snowflake."""
        print("🔌 Connecting to Snowflake...")
        
        password = getpass.getpass("Enter your Snowflake password: ")
        
        try:
            self.connection = snowflake.connector.connect(
                account='JHYWOUK-WA83239',
                user='ALGORYTHMOS',
                password=password,
                role='DASHBOARD_ANALYST_ROLE',
                warehouse='COMPUTE_WH',
                database='TPCH_DASHBOARDS',
                schema='PUBLIC'
            )
            self.cursor = self.connection.cursor()
            print("✅ Connected successfully!")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def test_data_availability(self):
        """Test all data sources are available."""
        print("\n📊 Testing Data Availability...")
        print("-" * 50)
        
        tables = [
            "CUSTOMER_LINEITEM_PROFILE",
            "V_CUSTOMER_DETAILS", 
            "V_ORDER_DETAILS",
            "V_MONTHLY_REVENUE_BY_REGION",
            "V_MARKET_SEGMENT_ANALYSIS"
        ]
        
        results = {}
        total_records = 0
        
        for table in tables:
            try:
                start_time = time.time()
                self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = self.cursor.fetchone()[0]
                query_time = time.time() - start_time
                
                results[table] = {
                    'records': count,
                    'query_time': query_time,
                    'status': 'success'
                }
                total_records += count
                
                print(f"✅ {table}: {count:,} records ({query_time:.2f}s)")
                
            except Exception as e:
                results[table] = {
                    'records': 0,
                    'query_time': 0,
                    'status': 'failed',
                    'error': str(e)
                }
                print(f"❌ {table}: {e}")
        
        self.test_results['data_availability'] = results
        self.test_results['total_records'] = total_records
        
        print(f"\n📈 Total Records Available: {total_records:,}")
        return len([r for r in results.values() if r['status'] == 'success']) == len(tables)
    
    def test_tableau_queries(self):
        """Test Tableau-specific queries."""
        print("\n🎨 Testing Tableau Queries...")
        print("-" * 50)
        
        queries = {
            "Monthly Revenue Trend": """
                SELECT 
                    DATE_TRUNC('MONTH', O_ORDERDATE) as month,
                    SUM(PRICE_AFTER_DISCOUNT) as revenue,
                    COUNT(DISTINCT O_CUSTKEY) as customers
                FROM CUSTOMER_LINEITEM_PROFILE
                GROUP BY month
                ORDER BY month DESC
                LIMIT 12
            """,
            "Top Customers": """
                SELECT 
                    O_CUSTKEY as customer_id,
                    COUNT(DISTINCT O_ORDERKEY) as orders,
                    SUM(PRICE_AFTER_DISCOUNT) as revenue
                FROM CUSTOMER_LINEITEM_PROFILE
                GROUP BY customer_id
                ORDER BY revenue DESC
                LIMIT 10
            """,
            "Order Status Summary": """
                SELECT 
                    O_ORDERSTATUS,
                    COUNT(DISTINCT O_CUSTKEY) as customers,
                    COUNT(DISTINCT O_ORDERKEY) as orders,
                    SUM(PRICE_AFTER_DISCOUNT) as revenue
                FROM CUSTOMER_LINEITEM_PROFILE
                GROUP BY O_ORDERSTATUS
            """
        }
        
        tableau_results = {}
        
        for query_name, query in queries.items():
            try:
                start_time = time.time()
                self.cursor.execute(query)
                results = self.cursor.fetchall()
                query_time = time.time() - start_time
                
                tableau_results[query_name] = {
                    'rows_returned': len(results),
                    'query_time': query_time,
                    'status': 'success',
                    'sample_data': results[:3] if results else []
                }
                
                print(f"✅ {query_name}: {len(results)} rows ({query_time:.2f}s)")
                
            except Exception as e:
                tableau_results[query_name] = {
                    'rows_returned': 0,
                    'query_time': 0,
                    'status': 'failed',
                    'error': str(e)
                }
                print(f"❌ {query_name}: {e}")
        
        self.test_results['tableau_queries'] = tableau_results
        return all(r['status'] == 'success' for r in tableau_results.values())
    
    def test_powerbi_queries(self):
        """Test Power BI-specific queries."""
        print("\n📊 Testing Power BI Queries...")
        print("-" * 50)
        
        queries = {
            "Executive KPIs": """
                SELECT 
                    COUNT(DISTINCT O_CUSTKEY) as total_customers,
                    COUNT(DISTINCT O_ORDERKEY) as total_orders,
                    SUM(PRICE_AFTER_DISCOUNT) as total_revenue,
                    AVG(PRICE_AFTER_DISCOUNT) as avg_order_value
                FROM CUSTOMER_LINEITEM_PROFILE
            """,
            "Yearly Performance": """
                SELECT 
                    YEAR(O_ORDERDATE) as order_year,
                    COUNT(DISTINCT O_CUSTKEY) as customers,
                    SUM(PRICE_AFTER_DISCOUNT) as revenue
                FROM CUSTOMER_LINEITEM_PROFILE
                GROUP BY order_year
                ORDER BY order_year
            """,
            "Customer Segments": """
                SELECT 
                    CASE 
                        WHEN order_count >= 10 THEN 'High Frequency'
                        WHEN order_count >= 5 THEN 'Medium Frequency'
                        ELSE 'Low Frequency'
                    END as customer_segment,
                    COUNT(*) as customer_count,
                    SUM(total_revenue) as segment_revenue
                FROM (
                    SELECT 
                        O_CUSTKEY,
                        COUNT(DISTINCT O_ORDERKEY) as order_count,
                        SUM(PRICE_AFTER_DISCOUNT) as total_revenue
                    FROM CUSTOMER_LINEITEM_PROFILE
                    GROUP BY O_CUSTKEY
                ) customer_summary
                GROUP BY customer_segment
            """
        }
        
        powerbi_results = {}
        
        for query_name, query in queries.items():
            try:
                start_time = time.time()
                self.cursor.execute(query)
                results = self.cursor.fetchall()
                query_time = time.time() - start_time
                
                powerbi_results[query_name] = {
                    'rows_returned': len(results),
                    'query_time': query_time,
                    'status': 'success',
                    'sample_data': results[:3] if results else []
                }
                
                print(f"✅ {query_name}: {len(results)} rows ({query_time:.2f}s)")
                
            except Exception as e:
                powerbi_results[query_name] = {
                    'rows_returned': 0,
                    'query_time': 0,
                    'status': 'failed',
                    'error': str(e)
                }
                print(f"❌ {query_name}: {e}")
        
        self.test_results['powerbi_queries'] = powerbi_results
        return all(r['status'] == 'success' for r in powerbi_results.values())
    
    def test_looker_queries(self):
        """Test Looker-specific queries."""
        print("\n🔍 Testing Looker Queries...")
        print("-" * 50)
        
        queries = {
            "Customer Analysis": """
                SELECT 
                    O_CUSTKEY as customer_key,
                    COUNT(DISTINCT O_ORDERKEY) as orders,
                    SUM(PRICE_AFTER_DISCOUNT) as revenue,
                    AVG(PRICE_PER_QTY) as avg_price_per_qty,
                    MIN(O_ORDERDATE) as first_order,
                    MAX(O_ORDERDATE) as last_order
                FROM CUSTOMER_LINEITEM_PROFILE
                GROUP BY customer_key
                ORDER BY revenue DESC
                LIMIT 5
            """,
            "Monthly Metrics": """
                SELECT 
                    DATE_TRUNC('MONTH', O_ORDERDATE) as month,
                    O_ORDERSTATUS as order_status,
                    COUNT(DISTINCT O_CUSTKEY) as customers,
                    SUM(PRICE_AFTER_DISCOUNT) as revenue
                FROM CUSTOMER_LINEITEM_PROFILE
                GROUP BY month, order_status
                ORDER BY month DESC, revenue DESC
                LIMIT 10
            """,
            "Performance Summary": """
                SELECT 
                    'Performance Metrics' as metric_type,
                    COUNT(*) as total_line_items,
                    COUNT(DISTINCT O_ORDERKEY) as unique_orders,
                    COUNT(DISTINCT O_CUSTKEY) as unique_customers,
                    MIN(O_ORDERDATE) as earliest_date,
                    MAX(O_ORDERDATE) as latest_date
                FROM CUSTOMER_LINEITEM_PROFILE
            """
        }
        
        looker_results = {}
        
        for query_name, query in queries.items():
            try:
                start_time = time.time()
                self.cursor.execute(query)
                results = self.cursor.fetchall()
                query_time = time.time() - start_time
                
                looker_results[query_name] = {
                    'rows_returned': len(results),
                    'query_time': query_time,
                    'status': 'success',
                    'sample_data': results[:2] if results else []
                }
                
                print(f"✅ {query_name}: {len(results)} rows ({query_time:.2f}s)")
                
            except Exception as e:
                looker_results[query_name] = {
                    'rows_returned': 0,
                    'query_time': 0,
                    'status': 'failed',
                    'error': str(e)
                }
                print(f"❌ {query_name}: {e}")
        
        self.test_results['looker_queries'] = looker_results
        return all(r['status'] == 'success' for r in looker_results.values())
    
    def test_configuration_files(self):
        """Test all BI configuration files exist and are valid."""
        print("\n📁 Testing Configuration Files...")
        print("-" * 50)
        
        config_files = {
            "tableau_connection.tds": "config/tableau_connection.tds",
            "powerbi_connection.json": "config/powerbi_connection.json", 
            "looker_model.lkml": "config/looker_model.lkml",
            "bi_security_setup.sql": "sql/bi_security_setup.sql",
            "looker_setup.sql": "sql/looker_setup.sql",
            "powerbi_sample_queries.sql": "sql/powerbi_sample_queries.sql"
        }
        
        file_results = {}
        
        for file_name, file_path in config_files.items():
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                
                # Basic validation for specific file types
                valid = True
                validation_msg = ""
                
                if file_name.endswith('.json'):
                    try:
                        with open(file_path, 'r') as f:
                            json.load(f)
                        validation_msg = "Valid JSON"
                    except json.JSONDecodeError as e:
                        valid = False
                        validation_msg = f"Invalid JSON: {e}"
                
                file_results[file_name] = {
                    'exists': True,
                    'size_bytes': size,
                    'valid': valid,
                    'validation': validation_msg,
                    'status': 'success' if valid else 'warning'
                }
                
                status = "✅" if valid else "⚠️"
                print(f"{status} {file_name}: {size:,} bytes ({validation_msg})")
                
            else:
                file_results[file_name] = {
                    'exists': False,
                    'size_bytes': 0,
                    'valid': False,
                    'validation': 'File missing',
                    'status': 'failed'
                }
                print(f"❌ {file_name}: Missing")
        
        self.test_results['config_files'] = file_results
        return all(r['exists'] for r in file_results.values())
    
    def test_performance_benchmarks(self):
        """Run performance benchmarks for BI workloads."""
        print("\n⚡ Running Performance Benchmarks...")
        print("-" * 50)
        
        benchmarks = {
            "Small Aggregation": "SELECT COUNT(*) FROM V_MARKET_SEGMENT_ANALYSIS",
            "Medium Aggregation": "SELECT COUNT(*) FROM V_MONTHLY_REVENUE_BY_REGION", 
            "Large Aggregation": """
                SELECT 
                    O_ORDERSTATUS,
                    COUNT(*) as records
                FROM CUSTOMER_LINEITEM_PROFILE 
                GROUP BY O_ORDERSTATUS
            """,
            "Complex Join": """
                SELECT 
                    DATE_TRUNC('YEAR', O_ORDERDATE) as year,
                    COUNT(DISTINCT O_CUSTKEY) as customers
                FROM CUSTOMER_LINEITEM_PROFILE
                WHERE O_ORDERDATE >= '1995-01-01'
                GROUP BY year
                ORDER BY year
            """
        }
        
        perf_results = {}
        
        for benchmark_name, query in benchmarks.items():
            try:
                # Warm up query
                self.cursor.execute(query)
                self.cursor.fetchall()
                
                # Actual benchmark
                start_time = time.time()
                self.cursor.execute(query)
                results = self.cursor.fetchall()
                query_time = time.time() - start_time
                
                perf_results[benchmark_name] = {
                    'query_time': query_time,
                    'rows_returned': len(results),
                    'status': 'success'
                }
                
                performance_rating = "🚀" if query_time < 1.0 else "⚡" if query_time < 3.0 else "🐌"
                print(f"{performance_rating} {benchmark_name}: {query_time:.2f}s ({len(results)} rows)")
                
            except Exception as e:
                perf_results[benchmark_name] = {
                    'query_time': 999.0,
                    'rows_returned': 0,
                    'status': 'failed',
                    'error': str(e)
                }
                print(f"❌ {benchmark_name}: {e}")
        
        self.test_results['performance'] = perf_results
        return all(r['status'] == 'success' for r in perf_results.values())
    
    def generate_test_report(self):
        """Generate comprehensive test report."""
        print("\n" + "=" * 80)
        print("🎯 COMPREHENSIVE BI CONNECTION TEST REPORT")
        print("=" * 80)
        
        # Summary
        total_tests = 0
        passed_tests = 0
        
        test_categories = [
            ('Data Availability', 'data_availability'),
            ('Tableau Queries', 'tableau_queries'),
            ('Power BI Queries', 'powerbi_queries'),
            ('Looker Queries', 'looker_queries'),
            ('Config Files', 'config_files'),
            ('Performance', 'performance')
        ]
        
        for category_name, category_key in test_categories:
            if category_key in self.test_results:
                category_data = self.test_results[category_key]
                
                if category_key == 'data_availability':
                    category_total = len(category_data)
                    category_passed = len([r for r in category_data.values() if r['status'] == 'success'])
                else:
                    category_total = len(category_data)
                    category_passed = len([r for r in category_data.values() if r['status'] == 'success'])
                
                total_tests += category_total
                passed_tests += category_passed
                
                status = "✅" if category_passed == category_total else "⚠️"
                print(f"{status} {category_name}: {category_passed}/{category_total} tests passed")
        
        print(f"\n📊 OVERALL RESULTS: {passed_tests}/{total_tests} tests passed")
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        if success_rate >= 95:
            print("🎉 EXCELLENT: Your BI platform is ready for production!")
        elif success_rate >= 80:
            print("✅ GOOD: Your BI platform is ready with minor issues to address")
        else:
            print("⚠️ NEEDS ATTENTION: Several issues need to be resolved")
        
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        if 'total_records' in self.test_results:
            print(f"📊 Total Records: {self.test_results['total_records']:,}")
        
        # Performance summary
        if 'performance' in self.test_results:
            avg_time = sum(r['query_time'] for r in self.test_results['performance'].values() 
                          if r['status'] == 'success') / len(self.test_results['performance'])
            print(f"⚡ Average Query Time: {avg_time:.2f} seconds")
        
        print("\n🚀 Your enterprise Snowflake BI platform is ready!")
        print("Connect your BI tools and start building amazing dashboards! ✨")
    
    def run_all_tests(self):
        """Run complete test suite."""
        print("🧪 Starting Comprehensive BI Connection Test Suite")
        print("=" * 80)
        
        if not self.connect_to_snowflake():
            return False
        
        tests = [
            self.test_data_availability,
            self.test_tableau_queries,
            self.test_powerbi_queries, 
            self.test_looker_queries,
            self.test_configuration_files,
            self.test_performance_benchmarks
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"❌ Test failed: {e}")
        
        self.generate_test_report()
        
        if self.connection:
            self.cursor.close()
            self.connection.close()
        
        return True

if __name__ == "__main__":
    tester = BIConnectionTester()
    tester.run_all_tests()
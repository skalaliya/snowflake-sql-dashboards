#!/usr/bin/env python3
"""
Snowflake SQL Deployment Script

Runs all SQL files in the sql/ directory in lexicographic order.
Requires environment variables or .env file with Snowflake credentials.
"""

import os
import sys
from pathlib import Path
import snowflake.connector
from dotenv import load_dotenv


def get_connection_params():
    """Get Snowflake connection parameters from environment variables."""
    load_dotenv()
    
    required_params = ['SNOW_ACCOUNT', 'SNOW_USER', 'SNOW_PASSWORD']
    missing_params = [p for p in required_params if not os.getenv(p)]
    
    if missing_params:
        print(f"Error: Missing required environment variables: {', '.join(missing_params)}")
        print("Please set them in your environment or create a .env file")
        sys.exit(1)
    
    params = {
        'account': os.getenv('SNOW_ACCOUNT'),
        'user': os.getenv('SNOW_USER'),
        'password': os.getenv('SNOW_PASSWORD'),
    }
    
    # Optional parameters
    if os.getenv('SNOW_ROLE'):
        params['role'] = os.getenv('SNOW_ROLE')
    if os.getenv('SNOW_WAREHOUSE'):
        params['warehouse'] = os.getenv('SNOW_WAREHOUSE')
    if os.getenv('SNOW_DATABASE'):
        params['database'] = os.getenv('SNOW_DATABASE')
    if os.getenv('SNOW_SCHEMA'):
        params['schema'] = os.getenv('SNOW_SCHEMA')
    
    return params


def get_sql_files(sql_dir):
    """Get all SQL files from directory in lexicographic order."""
    sql_path = Path(sql_dir)
    
    if not sql_path.exists():
        print(f"Error: SQL directory '{sql_dir}' does not exist")
        sys.exit(1)
    
    sql_files = sorted(sql_path.glob('*.sql'))
    
    if not sql_files:
        print(f"Warning: No SQL files found in '{sql_dir}'")
        return []
    
    return sql_files


def execute_sql_file(cursor, sql_file):
    """Execute SQL statements from a file."""
    print(f"\n{'='*60}")
    print(f"Executing: {sql_file.name}")
    print(f"{'='*60}")
    
    try:
        with open(sql_file, 'r') as f:
            sql_content = f.read()
        
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for i, statement in enumerate(statements, 1):
            # Skip empty statements and comments-only statements
            if not statement or all(line.strip().startswith('--') or not line.strip() 
                                   for line in statement.split('\n')):
                continue
            
            print(f"\nStatement {i}:")
            print(f"{statement[:100]}..." if len(statement) > 100 else statement)
            
            try:
                cursor.execute(statement)
                result = cursor.fetchall()
                if result:
                    print(f"Result: {result}")
                print("✓ Success")
            except Exception as e:
                print(f"✗ Error: {e}")
                raise
        
        print(f"\n✓ Completed: {sql_file.name}")
        
    except Exception as e:
        print(f"\n✗ Failed to execute {sql_file.name}: {e}")
        raise


def main():
    """Main deployment function."""
    print("="*60)
    print("Snowflake SQL Dashboard Deployment")
    print("="*60)
    
    # Get connection parameters
    print("\nConnecting to Snowflake...")
    conn_params = get_connection_params()
    
    # Mask password in display
    display_params = conn_params.copy()
    display_params['password'] = '***'
    print(f"Connection params: {display_params}")
    
    # Get SQL files
    sql_dir = Path(__file__).parent.parent / 'sql'
    sql_files = get_sql_files(sql_dir)
    
    if not sql_files:
        print("\nNo SQL files to execute. Exiting.")
        return
    
    print(f"\nFound {len(sql_files)} SQL file(s):")
    for sql_file in sql_files:
        print(f"  - {sql_file.name}")
    
    # Connect to Snowflake
    try:
        conn = snowflake.connector.connect(**conn_params)
        cursor = conn.cursor()
        
        print("\n✓ Connected to Snowflake")
        
        # Execute SQL files in order
        for sql_file in sql_files:
            execute_sql_file(cursor, sql_file)
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✓ Deployment completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Deployment failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

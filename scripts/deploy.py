#!/usr/bin/env python3
"""
Snowflake SQL Deployment Script

Runs all SQL files in the sql/ directory in lexicographic order.
Requires environment variables or .env file with Snowflake credentials.
"""

import argparse
import getpass
import logging
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import snowflake.connector
import sqlparse
from dotenv import load_dotenv


def setup_logging() -> None:
    """Configure logging for the deployment script."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Deploy Snowflake SQL files in lexicographic order"
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Print statements only, do not execute'
    )
    parser.add_argument(
        '--only', 
        type=str,
        help='Execute only this specific file (e.g., 07_sp_customer_profile.sql)'
    )
    parser.add_argument(
        '--stop-on-error', 
        action='store_true',
        help='Stop immediately on first error'
    )
    parser.add_argument(
        '--prompt-password',
        action='store_true',
        help='Prompt for password securely instead of using environment variable'
    )
    return parser.parse_args()


def get_connection_params(prompt_password: bool = False) -> Dict[str, str]:
    """Get Snowflake connection parameters from environment variables."""
    load_dotenv()
    
    # Check for required base parameters
    required_params = ['SNOW_ACCOUNT', 'SNOW_USER']
    missing_params = [p for p in required_params if not os.getenv(p)]
    
    if missing_params:
        logging.error(f"Missing required environment variables: {', '.join(missing_params)}")
        logging.error("Please set them in your environment or create a .env file")
        sys.exit(1)
    
    params = {
        'account': os.getenv('SNOW_ACCOUNT'),
        'user': os.getenv('SNOW_USER'),
    }
    
    # Handle authentication method
    authenticator = os.getenv('SNOW_AUTHENTICATOR', 'snowflake')
    if authenticator == 'externalbrowser':
        params['authenticator'] = 'externalbrowser'
    else:
        # Password authentication
        if prompt_password:
            password = getpass.getpass("Enter your Snowflake password: ")
            if not password.strip():
                logging.error("Password cannot be empty")
                sys.exit(1)
        else:
            password = os.getenv('SNOW_PASSWORD')
            if not password:
                logging.error("SNOW_PASSWORD is required when not using external browser authentication")
                logging.error("Use --prompt-password to enter password securely")
                sys.exit(1)
        params['password'] = password
    
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


def get_sql_files(sql_dir: Path, only_file: Optional[str] = None) -> List[Path]:
    """Get all SQL files from directory in lexicographic order."""
    if not sql_dir.exists():
        logging.error(f"SQL directory '{sql_dir}' does not exist")
        sys.exit(1)
    
    if only_file:
        only_path = sql_dir / only_file
        if not only_path.exists():
            logging.error(f"Specified file '{only_file}' not found in '{sql_dir}'")
            sys.exit(1)
        return [only_path]
    
    sql_files = sorted(sql_dir.glob('*.sql'))
    
    if not sql_files:
        logging.warning(f"No SQL files found in '{sql_dir}'")
        return []
    
    return sql_files


def is_comment_only_statement(statement: str) -> bool:
    """Check if statement contains only comments or whitespace."""
    lines = statement.strip().split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('--'):
            return False
    return True


def split_sql_statements(sql_content: str) -> List[str]:
    """Split SQL content into individual statements using sqlparse."""
    statements = []
    
    # Use sqlparse to split statements properly
    parsed_statements = sqlparse.split(sql_content)
    
    for stmt in parsed_statements:
        stmt = stmt.strip()
        if not stmt:
            continue
            
        # Skip pure comments
        if is_comment_only_statement(stmt):
            continue
            
        # Remove block comments
        stmt = re.sub(r'/\*.*?\*/', '', stmt, flags=re.DOTALL)
        stmt = stmt.strip()
        
        if stmt:
            statements.append(stmt)
    
    return statements


def execute_sql_file(
    cursor: snowflake.connector.cursor.SnowflakeCursor,
    sql_file: Path,
    dry_run: bool = False,
    stop_on_error: bool = True
) -> Tuple[int, int]:
    """Execute SQL statements from a file.
    
    Returns:
        Tuple of (successful_statements, total_statements)
    """
    logging.info(f"{'='*60}")
    logging.info(f"Processing: {sql_file.name}")
    logging.info(f"{'='*60}")
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        statements = split_sql_statements(sql_content)
        successful = 0
        total = len(statements)
        
        logging.info(f"Found {total} statements to execute")
        
        for i, statement in enumerate(statements, 1):
            logging.info(f"\nStatement {i}/{total}:")
            
            # Show statement snippet
            snippet = statement[:200] + "..." if len(statement) > 200 else statement
            logging.info(f"SQL: {snippet}")
            
            if dry_run:
                logging.info("(DRY RUN - not executed)")
                successful += 1
                continue
            
            try:
                cursor.execute(statement)
                result = cursor.fetchall()
                if result and len(result) <= 5:  # Show small results
                    logging.info(f"Result: {result}")
                elif result:
                    logging.info(f"Result: {len(result)} rows returned")
                logging.info("✓ Success")
                successful += 1
                
            except Exception as e:
                logging.error(f"✗ Error: {e}")
                logging.error(f"Failed statement: {statement[:500]}...")
                
                if stop_on_error:
                    raise
                else:
                    logging.warning("Continuing due to --stop-on-error=false")
        
        logging.info(f"\n✓ Completed: {sql_file.name} ({successful}/{total} statements)")
        return successful, total
        
    except Exception as e:
        logging.error(f"\n✗ Failed to process {sql_file.name}: {e}")
        raise


def main() -> None:
    """Main deployment function."""
    setup_logging()
    args = parse_args()
    
    # Check environment variables for flags
    dry_run = args.dry_run or os.getenv('DRY_RUN', '0') == '1'
    only_file = args.only or os.getenv('ONLY', '')
    stop_on_error = args.stop_on_error or os.getenv('STOP_ON_ERROR', '1') == '1'
    
    logging.info("="*60)
    logging.info("Snowflake SQL Dashboard Deployment")
    logging.info("="*60)
    
    if dry_run:
        logging.info("🔍 DRY RUN MODE - No SQL will be executed")
    if only_file:
        logging.info(f"📁 ONLY MODE - Processing file: {only_file}")
    if stop_on_error:
        logging.info("🛑 STOP ON ERROR - Will halt on first failure")
    else:
        logging.info("⚠️  CONTINUE ON ERROR - Will attempt all statements")
    
    # Get connection parameters
    logging.info("\nValidating connection parameters...")
    conn_params = get_connection_params(args.prompt_password)
    
    # Mask password in display
    display_params = conn_params.copy()
    display_params['password'] = '***'
    logging.info(f"Connection params: {display_params}")
    
    # Get SQL files
    sql_dir = Path(__file__).parent.parent / 'sql'
    sql_files = get_sql_files(sql_dir, only_file)
    
    if not sql_files:
        logging.info("No SQL files to execute. Exiting.")
        return
    
    logging.info(f"\nFound {len(sql_files)} SQL file(s):")
    for sql_file in sql_files:
        logging.info(f"  - {sql_file.name}")
    
    cursor = None
    conn = None
    
    try:
        # Connect to Snowflake
        if not dry_run:
            logging.info("\nConnecting to Snowflake...")
            conn = snowflake.connector.connect(**conn_params)
            cursor = conn.cursor()
            logging.info("✓ Connected to Snowflake")
        else:
            logging.info("\nSkipping Snowflake connection (dry run)")
        
        # Execute SQL files in order
        total_successful = 0
        total_statements = 0
        
        for sql_file in sql_files:
            successful, total = execute_sql_file(
                cursor, sql_file, dry_run, stop_on_error
            )
            total_successful += successful
            total_statements += total
        
        logging.info("\n" + "="*60)
        if dry_run:
            logging.info(f"✓ DRY RUN completed! Would execute {total_statements} statements")
        else:
            logging.info(f"✓ Deployment completed successfully!")
            logging.info(f"Executed {total_successful}/{total_statements} statements")
        logging.info("="*60)
        
    except Exception as e:
        logging.error(f"\n✗ Deployment failed: {e}")
        sys.exit(1)
        
    finally:
        # Clean up connections
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    main()

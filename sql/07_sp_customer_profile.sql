-- ============================================================================
-- Customer Profile Stored Procedure
-- ============================================================================
-- Python stored procedure to create customer profiles from TPCH data
-- Uses Snowpark-pandas for data transformation and creates both current and timestamped tables

CREATE OR REPLACE PROCEDURE CREATE_CUSTOMER_PROFILE_SP()
RETURNS VARCHAR
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python','pandas','pyarrow')
HANDLER = 'run'
AS
$$
import datetime as dt
import snowflake.snowpark as sp
from snowflake.snowpark.functions import col, lit, when

def run(session: sp.Session) -> str:
    try:
        # Read TPCH sources with Snowpark DataFrames (server-side processing)
        lineitem_df = session.table("SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.LINEITEM").select(
            col("L_ORDERKEY"),
            col("L_QUANTITY"), 
            col("L_EXTENDEDPRICE"),
            col("L_DISCOUNT"),
            col("L_RETURNFLAG")
        )
        
        orders_df = session.table("SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS").select(
            col("O_ORDERKEY"),
            col("O_CUSTKEY"),
            col("O_ORDERSTATUS"), 
            col("O_TOTALPRICE"),
            col("O_ORDERDATE")
        )
        
        # Filter out returned items and add calculated fields
        filtered_lineitem = lineitem_df.filter(col("L_RETURNFLAG") != "A").with_column(
            "DISCOUNT_AMOUNT",
            col("L_DISCOUNT") * col("L_QUANTITY") * col("L_EXTENDEDPRICE")
        )
        
        # Join lineitem with orders
        joined_df = filtered_lineitem.join(
            orders_df,
            filtered_lineitem["L_ORDERKEY"] == orders_df["O_ORDERKEY"],
            "inner"
        )
        
        # Add more feature engineering
        profile_df = joined_df.with_column(
            "PRICE_AFTER_DISCOUNT", 
            col("L_EXTENDEDPRICE") - col("DISCOUNT_AMOUNT")
        ).with_column(
            "PRICE_PER_QTY",
            when(col("L_QUANTITY") != 0, col("L_EXTENDEDPRICE") / col("L_QUANTITY")).otherwise(0)
        )
        
        # Create table names
        base_table = "CUSTOMER_LINEITEM_PROFILE"
        timestamp = dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        snapshot_table = f"{base_table}_{timestamp}"
        
        # Write current profile (replace existing)
        profile_df.write.mode("overwrite").save_as_table(base_table)
        
        # Write timestamped snapshot
        profile_df.write.mode("errorifexists").save_as_table(snapshot_table)
        
        # Get row count for confirmation
        row_count = profile_df.count()
        
        return f"✅ Success! Created {base_table} and {snapshot_table} with {row_count:,} rows"
        
    except Exception as e:
        return f"❌ Error: {str(e)}"
$$;
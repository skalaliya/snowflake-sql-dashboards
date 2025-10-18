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
import snowflake.snowpark.modin.pandas as pd

def run(session: sp.Session) -> str:
    # Read TPCH sources
    li_sp = session.table("SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.LINEITEM")[[
        "L_ORDERKEY","L_QUANTITY","L_EXTENDEDPRICE","L_DISCOUNT","L_RETURNFLAG"
    ]]
    orders_sp = session.table("SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS")[[
        "O_ORDERKEY","O_CUSTKEY","O_ORDERSTATUS","O_TOTALPRICE","O_ORDERDATE"
    ]]

    # Convert to Snowpark-pandas (pushdown stays in Snowflake)
    li = pd.DataFrame(li_sp)
    orders = pd.DataFrame(orders_sp)

    # Filter + feature engineering
    filtered = li[li["L_RETURNFLAG"] != "A"].assign(
        DISCOUNT_AMOUNT = li["L_DISCOUNT"] * li["L_QUANTITY"] * li["L_EXTENDEDPRICE"]
    )

    # Join with orders (rename to avoid col collisions)
    orders_ren = orders.rename(columns={"O_ORDERKEY":"ORDERKEY"})
    line_ren   = filtered.rename(columns={"L_ORDERKEY":"ORDERKEY"})
    joined = line_ren.merge(orders_ren, on="ORDERKEY", how="inner").assign(
        PRICE_AFTER_DISCOUNT = lambda df: df["L_EXTENDEDPRICE"] - df["DISCOUNT_AMOUNT"],
        PRICE_PER_QTY       = lambda df: df["L_EXTENDEDPRICE"] / (df["L_QUANTITY"].where(df["L_QUANTITY"]!=0, 1))
    )

    # Persist (latest + timestamped snapshot)
    base  = "CUSTOMER_LINEITEM_PROFILE"
    stamp = dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    snap  = f"{base}_{stamp}"

    joined.to_snowflake(base, index=False, if_exists="replace")
    joined.to_snowflake(snap, index=False, if_exists="fail")

    return f"wrote {base} and {snap} with {len(joined)} rows"
$$;
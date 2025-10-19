import snowflake.connector
import getpass

password = getpass.getpass("Enter password: ")
conn = snowflake.connector.connect(
    account='JHYWOUK-WA83239', user='ALGORYTHMOS', password=password,
    role='DASHBOARD_ANALYST_ROLE', warehouse='COMPUTE_WH', 
    database='TPCH_DASHBOARDS', schema='PUBLIC'
)
cursor = conn.cursor()
cursor.execute('DESCRIBE TABLE CUSTOMER_LINEITEM_PROFILE')
columns = cursor.fetchall()
print('Available columns in CUSTOMER_LINEITEM_PROFILE:')
for col in columns:
    print(f'  {col[0]} ({col[1]})')
cursor.close()
conn.close()
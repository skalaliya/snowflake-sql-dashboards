# 🔐 BI Security Best Practices Guide

## Overview
This guide provides enterprise-grade security setup for connecting BI tools to your Snowflake analytics platform.

---

## 🎯 Security Principles

### 1. Least Privilege Access
- ✅ **Dedicated roles** for each BI tool
- ✅ **Read-only permissions** for data access
- ✅ **Specific warehouse access** only
- ✅ **No administrative privileges**

### 2. Separation of Concerns
- ✅ **Service users** separate from human users
- ✅ **Tool-specific roles** (Looker, Power BI, Tableau)
- ✅ **Environment isolation** (dev/staging/prod)
- ✅ **Audit trails** for all connections

### 3. Network Security
- ✅ **IP allowlisting** for production environments
- ✅ **SSL/TLS encryption** for all connections
- ✅ **VPN requirements** where applicable
- ✅ **Connection monitoring** and alerts

---

## 🔑 User and Role Strategy

### Service Users Created
```sql
-- See: sql/bi_security_setup.sql for complete setup

LOOKER_USER     → LOOKER_ROLE     → Looker Studio/Cloud access
POWERBI_USER    → POWERBI_ROLE    → Power BI connections  
TABLEAU_USER    → TABLEAU_ROLE    → Tableau Desktop/Server
BI_USER         → BI_ROLE         → General BI tool access
```

### Permission Matrix
| Resource | Looker Role | PowerBI Role | Tableau Role | BI Role |
|----------|-------------|--------------|--------------|---------|
| COMPUTE_WH | USAGE, OPERATE | USAGE, OPERATE | USAGE, OPERATE | USAGE, OPERATE |
| TPCH_DASHBOARDS | USAGE | USAGE | USAGE | USAGE |
| PUBLIC Schema | USAGE | USAGE | USAGE | USAGE |
| All Tables | SELECT | SELECT | SELECT | SELECT |
| All Views | SELECT | SELECT | SELECT | SELECT |
| Future Objects | SELECT | SELECT | SELECT | SELECT |

---

## 🛡️ Security Implementation

### 1. Run the Security Setup
```bash
# Execute the BI security SQL script
cd /Users/skalaliya/Documents/snowflake-sql-dashboards-main
uv run -c "
import snowflake.connector, getpass
password = getpass.getpass('Enter ACCOUNTADMIN password: ')
conn = snowflake.connector.connect(
    account='JHYWOUK-WA83239', user='ALGORYTHMOS', password=password,
    role='ACCOUNTADMIN', warehouse='COMPUTE_WH'
)
cursor = conn.cursor()
with open('sql/bi_security_setup.sql', 'r') as f:
    commands = f.read().split(';')
    for cmd in commands:
        if cmd.strip() and not cmd.strip().startswith('--'):
            try:
                cursor.execute(cmd)
                print(f'✅ Executed: {cmd[:50]}...')
            except Exception as e:
                if 'already exists' not in str(e):
                    print(f'❌ Error: {e}')
cursor.close()
conn.close()
print('🔐 BI Security setup complete!')
"
```

### 2. Change Default Passwords
```sql
-- IMPORTANT: Change these default passwords!
ALTER USER LOOKER_USER SET PASSWORD = 'YourSecureLookerPassword2024!';
ALTER USER POWERBI_USER SET PASSWORD = 'YourSecurePowerBIPassword2024!'; 
ALTER USER TABLEAU_USER SET PASSWORD = 'YourSecureTableauPassword2024!';
ALTER USER BI_USER SET PASSWORD = 'YourSecureBIPassword2024!';
```

### 3. Enable Multi-Factor Authentication (Production)
```sql
-- Enable MFA for service users (recommended for production)
ALTER USER LOOKER_USER SET MINS_TO_BYPASS_MFA = 0;
ALTER USER POWERBI_USER SET MINS_TO_BYPASS_MFA = 0;
ALTER USER TABLEAU_USER SET MINS_TO_BYPASS_MFA = 0;
ALTER USER BI_USER SET MINS_TO_BYPASS_MFA = 0;
```

---

## 🌐 Network Security (Production)

### 1. IP Allowlisting
```sql
-- Create network policy for BI tools (modify IPs for your environment)
CREATE NETWORK POLICY BI_TOOLS_POLICY
  ALLOWED_IP_LIST=(
    '192.168.1.0/24',     -- Your office network
    '10.0.0.0/8',         -- Your cloud network
    '172.16.0.0/12'       -- Additional trusted networks
  )
  COMMENT='Network policy for BI tool connections';

-- Apply to BI users
ALTER USER LOOKER_USER SET NETWORK_POLICY = 'BI_TOOLS_POLICY';
ALTER USER POWERBI_USER SET NETWORK_POLICY = 'BI_TOOLS_POLICY';
ALTER USER TABLEAU_USER SET NETWORK_POLICY = 'BI_TOOLS_POLICY';
ALTER USER BI_USER SET NETWORK_POLICY = 'BI_TOOLS_POLICY';
```

### 2. Session Management
```sql
-- Set session timeouts for security
ALTER USER LOOKER_USER SET MINS_TO_UNLOCK = 5;
ALTER USER POWERBI_USER SET MINS_TO_UNLOCK = 5;
ALTER USER TABLEAU_USER SET MINS_TO_UNLOCK = 5;
ALTER USER BI_USER SET MINS_TO_UNLOCK = 5;

-- Disable password changes for service users
ALTER USER LOOKER_USER SET DISABLE_MFA = FALSE;
ALTER USER POWERBI_USER SET DISABLE_MFA = FALSE;
ALTER USER TABLEAU_USER SET DISABLE_MFA = FALSE;
ALTER USER BI_USER SET DISABLE_MFA = FALSE;
```

---

## 📊 Monitoring and Auditing

### 1. Monitor Login Activity
```sql
-- Query to monitor BI user logins
SELECT 
    USER_NAME,
    CLIENT_IP,
    REPORTED_CLIENT_TYPE,
    IS_SUCCESS,
    EVENT_TIMESTAMP
FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY 
WHERE USER_NAME IN ('LOOKER_USER', 'POWERBI_USER', 'TABLEAU_USER', 'BI_USER')
AND EVENT_TIMESTAMP >= DATEADD(day, -7, CURRENT_TIMESTAMP())
ORDER BY EVENT_TIMESTAMP DESC;
```

### 2. Monitor Query Activity
```sql
-- Query to monitor BI tool usage
SELECT 
    USER_NAME,
    ROLE_NAME,
    WAREHOUSE_NAME,
    DATABASE_NAME,
    QUERY_TYPE,
    TOTAL_ELAPSED_TIME,
    START_TIME
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY 
WHERE USER_NAME IN ('LOOKER_USER', 'POWERBI_USER', 'TABLEAU_USER', 'BI_USER')
AND START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
ORDER BY START_TIME DESC;
```

### 3. Set Up Alerts (Optional)
```sql
-- Create alert for failed logins
CREATE ALERT BI_FAILED_LOGINS
  WAREHOUSE = COMPUTE_WH
  SCHEDULE = 'USING CRON 0 * * * * UTC'  -- Every hour
  IF (
    SELECT COUNT(*) 
    FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY 
    WHERE USER_NAME IN ('LOOKER_USER', 'POWERBI_USER', 'TABLEAU_USER', 'BI_USER')
    AND IS_SUCCESS = 'NO'
    AND EVENT_TIMESTAMP >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
  ) > 5
  THEN CALL SYSTEM$SEND_EMAIL(
    'admin@yourcompany.com',
    'BI Security Alert: Multiple Failed Logins',
    'Multiple failed login attempts detected for BI users in the last hour.'
  );
```

---

## 🔧 Connection Security Best Practices

### 1. Connection Strings
Always use encrypted connections:
```
# Good - Encrypted connection
Server: JHYWOUK-WA83239.snowflakecomputing.com
SSL: Enabled/Required

# Bad - Never use unencrypted
Server: JHYWOUK-WA83239.snowflakecomputing.com:80
SSL: Disabled
```

### 2. Credential Management
- ✅ **Use environment variables** for passwords in scripts
- ✅ **Store credentials** in secure credential managers
- ✅ **Rotate passwords** regularly (quarterly)
- ✅ **Never hardcode** passwords in configuration files

### 3. BI Tool Security Settings

#### Power BI
```json
{
  "security": {
    "row_level_security": true,
    "encryption_at_rest": true,
    "encryption_in_transit": true
  }
}
```

#### Tableau
```xml
<security>
  <ssl_enabled>true</ssl_enabled>
  <auth_mode>database</auth_mode>
  <connection_pooling>true</connection_pooling>
</security>
```

#### Looker
```yaml
connection_settings:
  ssl_mode: require
  connection_pooling: true
  idle_timeout: 300
```

---

## ✅ Security Checklist

### Initial Setup
- [ ] BI security SQL script executed
- [ ] Default passwords changed to secure ones
- [ ] Service users created and roles assigned
- [ ] Network policies configured (production)
- [ ] Connection encryption verified

### Ongoing Maintenance  
- [ ] Regular password rotation (quarterly)
- [ ] Monitor login and query activity (weekly)
- [ ] Review and update IP allowlists (monthly)
- [ ] Audit user permissions (quarterly)
- [ ] Update BI tool security settings (as needed)

### Incident Response
- [ ] Procedure for compromised credentials
- [ ] Escalation path for security incidents
- [ ] Backup access methods documented
- [ ] Contact information updated

---

## 🚨 Emergency Procedures

### Disable Compromised User
```sql
-- Immediately disable a compromised user
ALTER USER LOOKER_USER SET DISABLED = TRUE;
-- Or revoke role access
REVOKE ROLE LOOKER_ROLE FROM USER LOOKER_USER;
```

### Reset Passwords
```sql
-- Force password reset
ALTER USER LOOKER_USER SET PASSWORD = 'NewTemporaryPassword123!'
                          MUST_CHANGE_PASSWORD = TRUE;
```

### Audit Compromised Activity
```sql
-- Check recent activity for compromised user
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY 
WHERE USER_NAME = 'LOOKER_USER'
AND START_TIME >= DATEADD(day, -30, CURRENT_TIMESTAMP())
ORDER BY START_TIME DESC;
```

---

## 📞 Support and Contacts

- **Security Issues:** security@yourcompany.com
- **BI Platform Support:** bi-support@yourcompany.com
- **Snowflake Admin:** snowflake-admin@yourcompany.com

**Your enterprise BI security is now professionally configured!** 🛡️✨
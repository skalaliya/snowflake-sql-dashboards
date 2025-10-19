#!/bin/bash
# GitHub Secrets Setup Helper
# This script shows you the exact commands to add secrets via GitHub CLI

echo "🔐 GitHub Secrets Setup for Snowflake Deployment"
echo "================================================="
echo
echo "📋 You need to add these 7 secrets to your GitHub repository:"
echo
echo "1. SNOW_ACCOUNT = JHYWOUK-WA83239"
echo "2. SNOW_USER = ALGORYTHMOS" 
echo "3. SNOW_PASSWORD = [your_snowflake_password]"
echo "4. SNOW_ROLE = ACCOUNTADMIN"
echo "5. SNOW_WAREHOUSE = COMPUTE_WH"
echo "6. SNOW_DATABASE = TPCH_DASHBOARDS"
echo "7. SNOW_SCHEMA = PUBLIC"
echo
echo "🌐 Via GitHub Web UI:"
echo "   1. Go to: https://github.com/skalaliya/snowflake-sql-dashboards/settings/secrets/actions"
echo "   2. Click 'New repository secret' for each one"
echo "   3. Copy the name and value exactly as shown above"
echo
echo "💻 Via GitHub CLI (if you have gh installed):"
echo
echo "gh secret set SNOW_ACCOUNT --body 'JHYWOUK-WA83239'"
echo "gh secret set SNOW_USER --body 'ALGORYTHMOS'"
echo "gh secret set SNOW_PASSWORD --body 'YOUR_ACTUAL_PASSWORD_HERE'"
echo "gh secret set SNOW_ROLE --body 'ACCOUNTADMIN'"
echo "gh secret set SNOW_WAREHOUSE --body 'COMPUTE_WH'"
echo "gh secret set SNOW_DATABASE --body 'TPCH_DASHBOARDS'"
echo "gh secret set SNOW_SCHEMA --body 'PUBLIC'"
echo
echo "✅ Once added, your next git push will trigger automatic deployment!"
echo
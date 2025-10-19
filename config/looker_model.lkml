# LookML Model for Snowflake Analytics Platform
# Place this in your Looker project

connection: "snowflake_analytics"
label: "Snowflake Analytics Platform"

include: "/views/*.view.lkml"
include: "/dashboards/*.dashboard.lookml"

datagroup: analytics_default_datagroup {
  sql_trigger: SELECT MAX(O_ORDERDATE) FROM PUBLIC.CUSTOMER_LINEITEM_PROFILE;;
  max_cache_age: "4 hours"
  description: "Data refreshes when new orders are processed"
}

persist_with: analytics_default_datagroup

# Main Customer Profile Explore
explore: customer_lineitem_profile {
  label: "Customer & Order Analysis"
  description: "Complete customer order profile with 4.5M+ records"
  
  dimension: customer_key {
    type: number
    primary_key: yes
    sql: ${TABLE}.O_CUSTKEY ;;
    label: "Customer ID"
  }
  
  dimension: order_key {
    type: number
    sql: ${TABLE}.O_ORDERKEY ;;
    label: "Order ID"
  }
  
  dimension_group: order {
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    sql: ${TABLE}.O_ORDERDATE ;;
    label: "Order"
  }
  
  dimension: region {
    type: string
    sql: ${TABLE}.N_NAME ;;
    label: "Region"
    map_layer_name: world_countries
  }
  
  dimension: market_segment {
    type: string
    sql: ${TABLE}.C_MKTSEGMENT ;;
    label: "Market Segment"
  }
  
  measure: total_revenue {
    type: sum
    sql: ${TABLE}.PRICE_AFTER_DISCOUNT ;;
    label: "Total Revenue"
    value_format_name: usd
    drill_fields: [customer_key, order_key, order_date, region, market_segment]
  }
  
  measure: average_price_per_qty {
    type: average
    sql: ${TABLE}.PRICE_PER_QTY ;;
    label: "Average Price per Quantity"
    value_format_name: usd
  }
  
  measure: customer_count {
    type: count_distinct
    sql: ${TABLE}.O_CUSTKEY ;;
    label: "Unique Customers"
  }
  
  measure: order_count {
    type: count_distinct
    sql: ${TABLE}.O_ORDERKEY ;;
    label: "Total Orders"
  }
  
  measure: average_order_value {
    type: number
    sql: ${total_revenue} / NULLIF(${order_count}, 0) ;;
    label: "Average Order Value"
    value_format_name: usd
  }
}

# Customer Details View
view: customer_details {
  sql_table_name: PUBLIC.V_CUSTOMER_DETAILS ;;
  label: "Customer Demographics"
  
  dimension: customer_key {
    type: number
    primary_key: yes
    sql: ${TABLE}.C_CUSTKEY ;;
  }
  
  dimension: customer_name {
    type: string
    sql: ${TABLE}.C_NAME ;;
  }
  
  dimension: phone {
    type: string
    sql: ${TABLE}.C_PHONE ;;
  }
  
  dimension: account_balance {
    type: number
    sql: ${TABLE}.C_ACCTBAL ;;
    value_format_name: usd
  }
  
  dimension: market_segment {
    type: string
    sql: ${TABLE}.C_MKTSEGMENT ;;
  }
  
  dimension: nation {
    type: string
    sql: ${TABLE}.N_NAME ;;
    map_layer_name: world_countries
  }
  
  dimension: region {
    type: string
    sql: ${TABLE}.R_NAME ;;
  }
}

# Regional Revenue Analysis
view: monthly_revenue_by_region {
  sql_table_name: PUBLIC.V_MONTHLY_REVENUE_BY_REGION ;;
  label: "Regional Revenue Trends"
  
  dimension_group: order {
    type: time
    timeframes: [date, week, month, quarter, year]
    sql: ${TABLE}.O_ORDERDATE ;;
  }
  
  dimension: region {
    type: string
    sql: ${TABLE}.N_NAME ;;
    map_layer_name: world_countries
  }
  
  measure: monthly_revenue {
    type: sum
    sql: ${TABLE}.TOTAL_REVENUE ;;
    value_format_name: usd
  }
  
  measure: order_count {
    type: sum
    sql: ${TABLE}.ORDER_COUNT ;;
  }
}

# Market Segment Analysis
view: market_segment_analysis {
  sql_table_name: PUBLIC.V_MARKET_SEGMENT_ANALYSIS ;;
  label: "Market Segment Performance"
  
  dimension: market_segment {
    type: string
    sql: ${TABLE}.C_MKTSEGMENT ;;
  }
  
  measure: segment_revenue {
    type: sum
    sql: ${TABLE}.TOTAL_REVENUE ;;
    value_format_name: usd
  }
  
  measure: customer_count {
    type: sum
    sql: ${TABLE}.CUSTOMER_COUNT ;;
  }
  
  measure: average_customer_value {
    type: number
    sql: ${segment_revenue} / NULLIF(${customer_count}, 0) ;;
    value_format_name: usd
  }
}
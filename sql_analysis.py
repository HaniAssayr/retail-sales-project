
import sqlite3
import pandas as pd

conn = sqlite3.connect("retail_sales.db")

# 1. Top 10 products by revenue
query = """
SELECT Description, ROUND(SUM(Revenue), 2) AS total_revenue
FROM sales
GROUP BY Description
ORDER BY total_revenue DESC
LIMIT 10;
"""
print("\nTop 10 Products")
print(pd.read_sql_query(query, conn))

# 2. Top 10 months by revenue
query = """
SELECT strftime('%Y-%m', InvoiceDate) AS sales_month,
       ROUND(SUM(Revenue), 2) AS total_revenue
FROM sales
GROUP BY sales_month
ORDER BY total_revenue DESC
LIMIT 10;
"""
print("\nTop 10 Months")
print(pd.read_sql_query(query, conn))

# 3. Top 10 countries by revenue
query = """
SELECT Country, ROUND(SUM(Revenue), 2) AS total_revenue
FROM sales
GROUP BY Country
ORDER BY total_revenue DESC
LIMIT 10;
"""
print("\nTop 10 Countries")
print(pd.read_sql_query(query, conn))

# 4. JOIN practice: revenue by region
countries = pd.read_sql_query(
    "SELECT DISTINCT Country FROM sales", conn
)
countries["Region"] = "Other"
countries.loc[countries["Country"] == "United Kingdom", "Region"] = "UK"

countries.to_sql("country_regions", conn, if_exists="replace", index=False)

query = """
SELECT c.Region, ROUND(SUM(s.Revenue), 2) AS total_revenue
FROM sales AS s
JOIN country_regions AS c ON s.Country = c.Country
GROUP BY c.Region
ORDER BY total_revenue DESC;
"""
print("\nRevenue by Region (JOIN)")
print(pd.read_sql_query(query, conn))

conn.close()

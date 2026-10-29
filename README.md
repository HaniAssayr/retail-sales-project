# Retail Sales Analysis

## Project Overview
This project analyzes online retail sales data using Python to identify sales trends, top-performing products, and leading markets.

## Data Cleaning
- Removed duplicate records.
- Excluded cancelled transactions from ordinary sales analysis.
- Excluded rows with non-positive quantities or prices.
- Excluded selected non-product transactions, including postage, fees, and accounting adjustments.

## Key Findings
- **Total product revenue:** 10,255,184.18
- **Top product by revenue:** REGENCY CAKESTAND 3 TIER — 174,156.54
- **Best-performing month:** November 2011 — 1,453,295.98
- **Top country:** United Kingdom — 8,726,832.53

## Tools Used
- Python
- Pandas
- Matplotlib
- PyCharm

## Visualizations
Charts showing monthly revenue, top countries and the top 10 products by revenue will be included here.

### Monthly Revenue
![Monthly Revenue](monthly_revenue.png)

### Top 10 Products by Revenue
![Top Products](top_products.png)

### Top 10 Countries by Revenue
![Top Countries](top_countries.png)

## SQL Business Analysis

### 1. Which products generate the most revenue?
- Regency Cakestand 3 Tier ranked first, generating **174,156.54** in revenue.
- Paper Craft, Little Birdie ranked second, generating **168,469.60**.

### 2. Which month generates the most revenue?
- **November 2011** was the highest-revenue month, generating **1,453,295.98**.

### 3. Which countries generate the most revenue?
- The **United Kingdom** ranked first, generating **8,726,832.53**.
- The Netherlands ranked second, generating **283,889.34**.

*Note: Revenue figures reflect the project's data-cleaning rules and are not necessarily official accounting revenue.*

## SQL Analysis

### Objective
Analyze retail sales data using SQLite and SQL to identify revenue trends across products, months, and countries.

### Tools
Python, Pandas, SQLite, SQL.

### Key Findings
- **Top Product:** Regency Cakestand 3 Tier — 174,156.54 revenue.
- **Best Month:** November 2011 — 1,453,295.98 revenue.
- **Top Country:** United Kingdom — 8,726,832.53 revenue.

### SQL Skills
- Aggregation using `SUM()` and `GROUP BY`
- Sorting and ranking using `ORDER BY` and `LIMIT`
- Monthly analysis using `strftime()`
- Combining tables using `JOIN`

### Conclusion
SQL analysis identified the leading products, strongest sales month, and highest-revenue country, complementing the project's Python analysis.

*Revenue figures reflect the project's data-cleaning rules.
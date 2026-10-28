import pandas as pd

# sales = pd.read_csv("salea_transaction_2022_2025.csv")
df = pd.read_csv("Retail_data.csv",encoding="cp1252")

# Explore the values:
# print("Duplicated values:", df.duplicated().sum())
# print(df.describe())
# print(df["Country"].value_counts().head(10))
# print("Unique invoices:", df["InvoiceNo"].nunique())
# print("Unique products:", df["StockCode"].nunique())
# print("Unique customers:", df["CustomerID"].nunique())
# print("Date range:", df["InvoiceDate"].min(),
#       "to", df["InvoiceDate"].max())

# checking the missing:
print(df.isnull().sum())
print((df.isnull().mean() * 100).round(2))

# checking duplicated values:
# print("Duplicate rows:", df.duplicated().sum())
before= len(df)
df= df.drop_duplicates().copy()
# print("Rows removed:", before-len(df))
# print("duplicates remaining:", df.duplicated().sum())
# print("Rows after cleaning:", len(df))


# checking cancellations:

cancelled= df[df
    ['InvoiceNo'].astype(str).str.startswith("C")]
print("Cancelled transections rows:", len(cancelled))
print("Negative quantity rows:", (df["Quantity"] < 0).sum())
print("Negative price rows:", (df["UnitPrice"] < 0).sum())

print(df[df["UnitPrice"] < 0][
    ["InvoiceNo", "Description", "Quantity", "UnitPrice"]
])
print("Zero-price rows:", (df["UnitPrice"] == 0).sum())

zero_prices = df[df["UnitPrice"] == 0]

# print(zero_prices["Description"].value_counts().head(10))

# checking date:
# print(df["InvoiceDate"].dtype)

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    format="%m/%d/%Y %H:%M"
)

# print(df["InvoiceDate"].dtype)
#
# print("Earliest date:", df["InvoiceDate"].min())
# print("Latest date:", df["InvoiceDate"].max())
#
# print("Unique products:", df["StockCode"].nunique())
# print("Unique invoices:", df["InvoiceNo"].nunique())
# print("Unique customers:", df["CustomerID"].nunique())
#
# print(df["Country"].nunique())
# print(df["Country"].value_counts().head(10))
#
# print(df[df["Description"].isnull()].head())
#
# print(
#     df[df["Description"].isnull()]["StockCode"].nunique()
# )
#
# print(df[df["CustomerID"].isnull()][
#     ["InvoiceNo", "Quantity", "UnitPrice", "Country"]
# ].head())
#
# print(df.isnull().sum())

# preparing data:

# handling cancellations: through saprations of cancelled and reqular transactions:

is_cancelled = df["InvoiceNo"].astype(str).str.startswith("C")

Cancelled= df[is_cancelled].copy()

sales= df[~is_cancelled].copy()

print('Cancelled row:', len(Cancelled))
print("Regular transactions:", len(sales))

# Find negative quantities in regular transactions
negative_sales = sales[sales["Quantity"] < 0]

print("Negative quantities in regular transactions:",
      len(negative_sales))

print(negative_sales[["InvoiceNo", "StockCode", "Quantity", "UnitPrice"]].head(10))

# Investigate negative quantities in regular transactions
# print("Negative quantity rows:", len(negative_sales))
#
# print("\nUnit price distribution:")
# print(negative_sales["UnitPrice"].value_counts().head(10))
#
# print("\nDescriptions:")
# print(negative_sales["Description"].value_counts().head(10))
#
# print("\nInvoice numbers:")
# print(negative_sales["InvoiceNo"].head(20).to_list())

sales_clean = sales[
    (sales["Quantity"] > 0) &
    (sales["UnitPrice"] > 0)
].copy()

print("Rows before:", len(sales))
print("Rows after:", len(sales_clean))

sales_clean["Revenue"] = (
    sales_clean["Quantity"] * sales_clean["UnitPrice"]
)

# print("Total revenue:", round(sales_clean["Revenue"].sum(), 2))

top_products = (
    sales_clean.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# print(top_products)

monthly_sales = (
    sales_clean.groupby(
        sales_clean["InvoiceDate"].dt.to_period("M")
    )["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

# print(monthly_sales)

country_sales = (
    sales_clean.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# print(country_sales)

cancelled["Revenue"] = cancelled["Quantity"] * cancelled["UnitPrice"]

# print("Cancelled rows:", len(cancelled))
# print("Cancellation value:", round(cancelled["Revenue"].sum(), 2))

returns_or_adjustments = sales[sales["Quantity"] < 0].copy()

returns_or_adjustments["Revenue"] = (
    returns_or_adjustments["Quantity"] *
    returns_or_adjustments["UnitPrice"]
)

# print("Negative-quantity rows:", len(returns_or_adjustments))
# print("Recorded value:", round(returns_or_adjustments["Revenue"].sum(), 2))

# Reviewing the cleaning result:
#
# print("Original rows:", len(df))
# print("Sales rows before cleaning:", len(sales))
# print("Sales rows after cleaning:", len(sales_clean))
#
# print("\nRemaining negative quantities:")
# print((sales_clean["Quantity"] < 0).sum())
#
# print("\nRemaining zero or negative prices:")
# print((sales_clean["UnitPrice"] <= 0).sum())
#
# print("\nMissing descriptions:")
# print(sales_clean["Description"].isna().sum())

# Checking for other unusual records

print("\nTop 10 largest quantities:")
print(
    sales_clean.nlargest(10, "Quantity")[
        ["Description", "Quantity", "UnitPrice", "Revenue"]
    ]
)

print("\nTop 10 highest unit prices:")
print(
    sales_clean.nlargest(10, "UnitPrice")[
        ["Description", "Quantity", "UnitPrice", "Revenue"]
    ]
)


unusual_items = sales_clean[
    sales_clean["Description"].str.contains(
        "AMAZON FEE|Adjust bad debt|POSTAGE|Manual",
        case=False,
        na=False
    )
]

print(
    unusual_items.groupby("Description")
    .agg(
        Transactions=("InvoiceNo", "count"),
        Total_Revenue=("Revenue", "sum")
    )
    .sort_values("Total_Revenue", ascending=False)
)

excluded_items = [
    "DOTCOM POSTAGE",
    "POSTAGE",
    "Manual",
    "AMAZON FEE",
    "Adjust bad debt"
]

product_sales = sales_clean[
    ~sales_clean["Description"].isin(excluded_items)
].copy()
print("Rows before exclusion:", len(sales_clean))
print("Rows after exclusion:", len(product_sales))

# Calculating product Revenue:

total_revenue = product_sales["Revenue"].sum()

print("Total product revenue:", round(total_revenue, 2))

top_products = (
    product_sales.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# print(top_products)

product_sales["Month"] = (
    product_sales["InvoiceDate"].dt.to_period("M")
)

monthly_revenue = (
    product_sales.groupby("Month")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

# print(monthly_revenue)

country_revenue = (
    product_sales.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# print(country_revenue)

# Visualization


import matplotlib.pyplot as plt

monthly_chart = (
    product_sales.groupby(
        product_sales["InvoiceDate"].dt.to_period("M")
    )["Revenue"].sum()
)

monthly_chart.index = monthly_chart.index.astype(str)

monthly_chart.plot(kind="bar", figsize=(10, 5))

plt.title("Monthly Product Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
# plt.show()

# visualizing top products by revenue:

top_products.plot(kind="bar", figsize=(10, 5))

plt.title("Top 10 Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.ticklabel_format(axis="y", style="plain")
plt.show()
print(top_products["CHILLI LIGHTS"])

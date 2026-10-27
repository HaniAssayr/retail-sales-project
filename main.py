import pandas as pd

# sales = pd.read_csv("salea_transaction_2022_2025.csv")
df = pd.read_csv("Retail_data.csv",encoding="cp1252")
print(df.head(5))
print(df.columns)


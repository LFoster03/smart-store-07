import pandas as pd
import sqlite3
import os

# === Paths ===
base_dir = r"C:\Projects\smart-store-07"
prepared_dir = os.path.join(base_dir, "data", "prepared")
dw_dir = os.path.join(base_dir, "data", "dw")
os.makedirs(dw_dir, exist_ok=True)

db_path = os.path.join(dw_dir, "smart_store.db")

# === Load cleaned data ===
customers_df = pd.read_csv(os.path.join(prepared_dir, "cleaned_customers.csv"))
products_df = pd.read_csv(os.path.join(prepared_dir, "cleaned_products.csv"))
sales_df = pd.read_csv(os.path.join(prepared_dir, "cleaned_sales.csv"))

# === Create SQLite DB ===
conn = sqlite3.connect(db_path)

# === Save dimension tables ===
customers_df.to_sql("dim_customers", conn, if_exists="replace", index=False)
products_df.to_sql("dim_products", conn, if_exists="replace", index=False)

# === Save fact table ===
sales_df.to_sql("fact_sales", conn, if_exists="replace", index=False)

# === Optional: Add indexes to improve performance ===
cursor = conn.cursor()
cursor.execute("CREATE INDEX IF NOT EXISTS idx_customer_id ON fact_sales (CustomerID);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_id ON fact_sales (ProductID);")

conn.commit()
conn.close()

print("✅ Data warehouse created at:", db_path)

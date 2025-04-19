import pandas as pd
import os

# === File paths ===
input_dir = r"C:\Projects\smart-store-07\data\raw"
output_dir = r"C:\Projects\smart-store-07\data\prepared"
os.makedirs(output_dir, exist_ok=True)

# === Load the CSV files ===
customers_df = pd.read_csv(os.path.join(input_dir, "customers_data.csv"))
products_df = pd.read_csv(os.path.join(input_dir, "products_data.csv"))
sales_df = pd.read_csv(os.path.join(input_dir, "sales_data.csv"))

# === Standardize column names ===
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

customers_df = clean_column_names(customers_df)
products_df = clean_column_names(products_df)
sales_df = clean_column_names(sales_df)

# === Remove duplicate rows ===
customers_df.drop_duplicates(inplace=True)
products_df.drop_duplicates(inplace=True)
sales_df.drop_duplicates(inplace=True)

# === Handle missing values ===
customers_df.dropna(subset=['customerid'], inplace=True)
products_df.dropna(subset=['productid'], inplace=True)
sales_df.dropna(subset=['transactionid', 'saledate'], inplace=True)

# === Format date columns ===
customers_df['birthdate'] = pd.to_datetime(customers_df['birthdate'], errors='coerce')
customers_df['joindate'] = pd.to_datetime(customers_df['joindate'], errors='coerce')
sales_df['saledate'] = pd.to_datetime(sales_df['saledate'], errors='coerce')

# === Extract year, month, and quarter from SaleDate ===
sales_df['sale_year'] = sales_df['saledate'].dt.year
sales_df['sale_month'] = sales_df['saledate'].dt.month
sales_df['sale_month_name'] = sales_df['saledate'].dt.strftime('%B')  # Optional: Full month name
sales_df['sale_quarter'] = sales_df['saledate'].dt.to_period('Q').astype(str)


if 'birthdate' in customers_df.columns:
    today = pd.Timestamp.today()
    birthdate = customers_df['birthdate']
    
    # Check if birthday has occurred this year
    has_had_birthday = (
        (today.month > birthdate.dt.month) |
        ((today.month == birthdate.dt.month) & (today.day >= birthdate.dt.day))
    )
    
    # Calculate age
    customers_df['age'] = today.year - birthdate.dt.year
    customers_df.loc[~has_had_birthday, 'age'] -= 1

    # Define age bins and labels
age_bins = [0, 17, 25, 35, 45, 60, 120]
age_labels = ['Under 18', '18-25', '26-35', '36-45', '46-60', '60+']

# Create age group column
customers_df['age_group'] = pd.cut(customers_df['age'], bins=age_bins, labels=age_labels, right=True)

# Optional: Fill missing or out-of-range with 'Unknown'
customers_df['age_group'] = customers_df['age_group'].cat.add_categories(['Unknown'])
customers_df['age_group'].fillna('Unknown', inplace=True)



# === Save cleaned data ===
customers_df.to_csv(os.path.join(output_dir, "cleaned_customers.csv"), index=False)
products_df.to_csv(os.path.join(output_dir, "cleaned_products.csv"), index=False)
sales_df.to_csv(os.path.join(output_dir, "cleaned_sales.csv"), index=False)

print("✅ Cleaning complete. Files saved to prepared folder.")

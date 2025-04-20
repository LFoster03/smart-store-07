"""
This script creates the data warehouse structure and loads data from cleaned CSVs.
"""

import sqlite3
import pandas as pd
import pathlib
import sys

# Project paths
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
PREPARED_DIR = PROJECT_ROOT / "data" / "prepared"
DW_DIR = PROJECT_ROOT / "data" / "dw"
DB_PATH = DW_DIR / "smart_store.db"

# Optional: add project root to sys.path for local module imports
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from utils.logger import logger  # Use your logger module

# Ensure output directory exists
DW_DIR.mkdir(parents=True, exist_ok=True)

# Delete existing DB if present
if DB_PATH.exists():
    try:
        DB_PATH.unlink()
        logger.info(f"Deleted existing database at {DB_PATH}")
    except Exception as e:
        logger.error(f"Could not delete existing database: {e}")

def create_tables(cursor: sqlite3.Cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_customers (
                customerid INTEGER PRIMARY KEY,
                name TEXT,
                region TEXT,
                joindate TEXT,
                birthdate TEXT,
                gender TEXT,
                age INTEGER,
                age_group TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_products (
                productid INTEGER PRIMARY KEY,
                productname TEXT,
                category TEXT,
                unitprice REAL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fact_sales (
                transactionid INTEGER PRIMARY KEY,
                saledate TEXT,
                customerid INTEGER,
                productid INTEGER,
                storeid INTEGER,
                campaignid INTEGER,
                saleamount REAL,
                sale_year INTEGER,
                sale_month INTEGER,
                sale_month_name TEXT,
                sale_quarter TEXT,
                FOREIGN KEY (customerid) REFERENCES dim_customers(customerid),
                FOREIGN KEY (productid) REFERENCES dim_products(productid)
            )
        """)

        logger.info("All tables created successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error creating tables: {e}")

def load_csv_to_table(conn, csv_path: pathlib.Path, table_name: str):
    try:
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        logger.info(f"Loaded data into {table_name} from {csv_path.name}")
    except Exception as e:
        logger.error(f"Failed to load {csv_path.name} into {table_name}: {e}")

def build_data_warehouse():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        create_tables(cursor)

        # Load data
        load_csv_to_table(conn, PREPARED_DIR / "cleaned_customers.csv", "dim_customers")
        load_csv_to_table(conn, PREPARED_DIR / "cleaned_products.csv", "dim_products")
        load_csv_to_table(conn, PREPARED_DIR / "cleaned_sales.csv", "fact_sales")

        conn.commit()
        conn.close()
        logger.info("Data warehouse creation and loading complete.")
    except Exception as e:
        logger.error(f"Unexpected error in warehouse build: {e}")

def main():
    logger.info("Starting data warehouse build...")
    build_data_warehouse()
    logger.info("Done.")

if __name__ == "__main__":
    main()

# smart-store-07
## Author: Lindsay Foster
## Date: April 2025
This project focuses on preparing and cleaning retail data from a fictional smart store for Business Intelligence (BI) and customer analytics. The dataset includes customer, product, and sales information.

# Section 1. The Business Goal
Analyze customers based on total spend and purchase frequency, then analyze where these high-value customers come from (regions) and what demographic traits they share (e.g., age, gender).
### Questions I want to answer:
1. Who are the store’s most valuable customers?

2. Where are they located?

3. What do they typically buy (category preferences)?

4. Do certain demographics tend to be more loyal or spend more?

# Create files and folders
.gitignore, requirements.txt, .venv, utils with logger.py, data folder with raw and prepared and scripts folder.
Then get the csv files and add data, then upload to data raw.

# Section 2. Data Source

## 📁 Files Involved: [smart-sales-raw-data](https://github.com/denisecase/smart-sales-raw-data/tree/main)

**Raw Data Files** (stored in `data/raw/`):
- `customers_data.csv`: Customer details including demographics.
- `products_data.csv`: Product information including category and pricing.
- `sales_data.csv`: Sales transactions linked to customers and products.

**Cleaned Output Files** (saved to `data/prepared/`):
- `cleaned_customers.csv`
- `cleaned_products.csv`
- `cleaned_sales.csv`

## 🧹 Data Cleaning and Transformation Steps

The script `scripts/prepare_data.py` performs the following operations:

### 1. 🔡 Standardize Column Names
- Converts all column headers to lowercase and replaces spaces with underscores for consistency.

### 2. 🧼 Remove Duplicates and Handle Missing Values
- Drops duplicate rows from all datasets.
- Removes records with missing critical IDs or date fields.

### 3. 🗓️ Format Date Columns
- Converts these fields into proper datetime format:
  - `birthdate`, `joindate` in `customers_data.csv`
  - `saledate` in `sales_data.csv`

### 4. 👵 Calculate Customer Age and Age Group
- Computes each customer's age from their birthdate.
- Adds a new `age_group` column with predefined age brackets:
  - Under 18, 18–25, 26–35, 36–45, 46–60, 60+

### 5. 📅 Add Date Features to Sales
- Extracts and adds the following from each `saledate`:
  - `sale_year` (e.g., 2024)
  - `sale_month` (e.g., 3)
  - `sale_month_name` (e.g., March)
  - `sale_quarter` (e.g., 2024Q1)

## 🛠️ How to Run

1. Make sure the raw data files are in `data/raw/`.
2. Run the script:

```bash
python scripts/prepare_data.py
```

# Section 3. Tools Used


Section 4. Workflow & Logic
Section 5. Results (narrative + visualizations)
Section 6. Suggested Business Action
Section 7. Challenges
Section 8. Ethical Considerations
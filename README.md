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
VS Code, Python, SQLite, ChatGPT, Power BI


# Section 4. Workflow & Logic
## Data Warehouse Creation
After cleaning the data, we organize it into a data warehouse using SQLite for analysis and reporting.
Data Warehouse Structure
Location:
data/dw/smart_store.db

Tables:

dim_customers – Dimension table containing enriched customer data (e.g., age, gender, region, age group).

dim_products – Dimension table with product details (name, category, unit price).

fact_sales – Fact table containing transaction-level sales data, including sale date, customer and product IDs, and sales breakdowns (e.g., year, month, quarter).

Steps Performed by scripts/create_data_warehouse.py
Loads cleaned datasets from data/prepared/:

cleaned_customers.csv

cleaned_products.csv

cleaned_sales.csv

Creates a new SQLite database at data/dw/smart_store.db.

Writes each dataset to a corresponding table:

dim_customers, dim_products, fact_sales

Adds indexes on key fields (e.g., CustomerID, ProductID) to optimize performance.

## Data Warehouse Creation & Loading
This step sets up a SQLite data warehouse in a star schema format and loads it with cleaned data from the data/prepared/ folder.

Star Schema Structure
Fact Table: fact_sales
Stores transactional sales data with keys linking to dimension tables and time breakdowns.

Dimension Tables:

dim_customers: Customer demographics and segmentation.

dim_products: Product categories and pricing.

Script Overview
The script scripts/dw_build.py handles:

Creation of Tables:

Creates fact and dimension tables using SQLite with appropriate relationships.

Loading Data:

Reads from the cleaned CSVs:

cleaned_customers.csv

cleaned_products.csv

cleaned_sales.csv

Loads them into their respective tables.

Output
A SQLite database is created at:
data/dw/smart_store.db

## OLAP Plan
### Business Goal
Identify and analyze high-value customer segments by region and demographics.
We want to discover who the most valuable customers are, where they are located, and what characteristics (like age group or gender) define them.

### Planned Visualizations and Outputs
1. Total Sales by Customer Region and Age Group
Title: Total Sales by Region and Age Group

Chart Type: Clustered Bar Chart

X-Axis: Customer Region

Y-Axis: Total Sales Amount

Legend: Age Groups (e.g., "18–25", "26–35", etc.)

Color Scheme: Use distinct colors for each age group for easy comparison

Why this chart?: Easy to compare how different age segments perform across regions.

2. High-Value Customer Count by Gender and Age Group
Title: Number of High-Value Customers by Gender and Age Group

Chart Type: Stacked Bar Chart

X-Axis: Age Group

Y-Axis: Number of Customers

Legend: Gender

Highlight: Use bold colors to highlight large segments.

Why this chart?: Reveals if loyalty and value are tied to certain demographic traits.

3. Category Preferences of High-Value Customers
Title: Preferred Product Categories of High-Value Customers

Chart Type: Pie Chart or Horizontal Bar Chart

Labels: Category Names

Values: % Share of Sales

Why this chart?: Helps marketing or product teams understand which products appeal to VIP customers.

4. Average Spend per Customer by Region
Title: Average Spend per Customer by Region

Chart Type: Column Chart

X-Axis: Region

Y-Axis: Avg. Spend per Customer (Total Spend / Unique Customers)

Why this chart?: Determines how profitable each region's customers are.

### Source Selection
Source: data/dw/smart_store.db
Use this SQLite data warehouse created in the earlier step.

Tables & Columns Needed
Tables:

fact_sales

dim_customers

dim_products

Columns:

From fact_sales: customer_id, product_id, sale_amount, sale_date

From dim_customers: region, gender, age_group

From dim_products: category

### Workflow Steps
Join fact_sales with dim_customers and dim_products

Aggregate total sales by:

Region & age group

Customer gender & age group

Product category

Region (for average spend)

Filter for high-value customers (e.g., customers with total spend above a certain threshold)

Calculate:

Total spend per customer

Average spend per region

Group and summarize for each chart as needed.

### Expected Outputs (Sample Columns)
region, age_group, total_sales

age_group, gender, customer_count

category, total_sales_by_vip_customers

region, avg_spend_per_customer

# Slicing, Dicing, and Drilldown using PowerBI and Python

## Python
### Slicing – Focus by Dimension
Filter for high-value customers only

Criteria: Customers with total spend > $1000 and purchase frequency > X

Implementation:

Group by customer_id, aggregate sale_amount

Filter to keep top customers (e.g., top 20% by spend)

```
python 
# Slice: High-value customers
high_value_customers = sales_df.groupby('customerid').agg(
    total_spent=('saleamount', 'sum'),
    purchases=('transactionid', 'count')
).reset_index()

top_spenders = high_value_customers[high_value_customers['total_spent'] > 1000]
```
#### Heatmap of High-Value Customer Sales by Region and Category
- Filtered the dataset to include only rows where `category == 'Electronics'`.
- Aggregated total sales within the filtered subset.

### Dicing – Break Down into Subcategories
Example: Analyze by Region and Category and then Region and Gender
Group by Region and Category then aggregate

Group by region, gender, then aggregate
```
python
# Dice: By Region and Gender
merged = top_spenders.merge(customers_df, on='customerid')
regional_breakdown = merged.groupby(['region', 'gender']).agg(
    avg_spent=('total_spent', 'mean'),
    customer_count=('customerid', 'nunique')
).reset_index()
```
Then group with all three and aggregate

### Drilldown – General to Specific
Analyze trends from Year → Quarter → Month

Approach:

Converted saledate to datetime and extracted year, month, and day.

Grouped sales by these components to reveal daily trends.

Created a composite date column for proper chronological sorting and visualization.

Use sales_df with time breakdown columns

Group by time hierarchy + demographics
```
# Drilldown: Year > Quarter > Month
time_trends = sales_df.merge(customers_df[['customerid', 'region']], on='customerid')
time_breakdown = time_trends.groupby(['sale_year', 'sale_quarter', 'sale_month_name', 'region']).agg(
    total_sales=('saleamount', 'sum')
).reset_index()
```

## Power BI
Power BI Setup Instructions
📥 1. Load Data
Import your CSVs into Power BI (customers.csv, sales.csv, products.csv).

Ensure relationships are set up:

sales.customerid → customers.customerid

sales.productid → products.productid

🔍 Slicing – Focus on High-Value Customers
💡 Business Question:
"Who are the store’s most valuable customers?"

🔧 Steps:
Create Measures:

DAX
TotalSpend = SUM('fact_sales'[saleamount])
PurchaseFrequency = COUNT('fact_sales'[transactionid])

Slicing: By Region, Gender, Age Group
- Slicers added for region, gender, and age_group for interactive filtering.
- Table view of customers with TotalSpend and PurchaseFrequency.

Dicing: Multi-dimensional Breakdown
- Bar chart of TotalSpend by region
- Column chart of TotalSpend by category
- tacked bar showing PurchaseFrequency by age_group and gender

Drilldown: From Year → Month → Day
- Grouped fact_sales by sale_year, sale_month, sale_day
- Created a date hierarchy for drilldown
- Used a line chart with drilldown to show daily sales trends over time

### Visualizing High-Value Customer Preferences
Customer Spend Table: A table visual showing each customer with their CustomerSpend, sorted descending to highlight the most valuable ones.

Sales by Category: A stacked bar chart showing which product categories high-value customers prefer. This was achieved by joining fact_sales with the products table and plotting total CustomerSpend per category.

Demographic Filters: Region, gender, and age group slicers were added to explore trends in loyalty and spending patterns.


# Section 5. Results (narrative + visualizations)
## Power BI
### Visualizations

1. ![Purchase frequency segmented by age group and gender.](olap\pics\PurchaseFreqbyAgeGender.png)

2. ![Spending patterns by day within each month.](olap\pics\SpendbyDayMonth.png)

3. ![Daily spend trends across the year. ](olap\pics\SpendbyDayYear.png)

4. ![Total spend segmented by gender.](olap\pics\SpendbyGender.png)

5. ![Total spend segmented by region.](olap\pics\SpendbyRegion.png)

6. ![Possibly total spend by product category (maybe filtered or with a different measure like sum vs. count)](olap\pics\SumSpendbyCategory.png)

7. ![Also shows spend by category; may vary from the previous based on aggregation logic or filters.](olap\pics\TotalSpendbyCategory.png)

### Results

1. Customer Segmentation by Age and Gender
(Visualization: PurchaseFreqbyAgeGender.png)

This chart analyzes purchase frequency across different age groups segmented by gender. A few notable trends emerged:

Age groups 25–34 and 35–44 showed the highest purchase activity, indicating a key target demographic.

Within these groups, female customers slightly outpaced males in frequency, suggesting higher engagement or loyalty.

Younger age groups (18–24), while active, had slightly lower frequency—potentially a growth area for targeted marketing.

This suggests that marketing strategies focusing on young to middle-aged adults, particularly females, may yield the greatest returns in repeat purchases.

2. Total Spend by Gender
(Visualization: SpendbyGender.png)

Spending by gender reveals that:

Males contributed slightly more in total spend than females.

This contrasts with the frequency chart, where females showed more frequent purchases—indicating males might be making fewer but higher-value transactions.

Segmented campaigns can capitalize on this by promoting high-ticket items to male customers and offering bundle or loyalty incentives to females for their frequent visits.

3. Regional Spend Patterns
(Visualization: SpendbyRegion.png)

The regional analysis highlights:

Central and West regions had the highest customer spend, indicating strong market presence and potentially larger or more loyal customer bases.

North and East regions trailed slightly, suggesting an opportunity for expansion or engagement initiatives.

Drilling into the customer base by region can help identify whether these differences stem from population size, store presence, or regional preferences.

4. Total Spend by Product Category
(Visuals: TotalSpendbyCategory.png, SumSpendbyCategory.png)

These charts explore customer preferences at the category level:

Electronics consistently drive the highest revenue, followed by Fitness products.

Spend is fairly distributed across categories, though accessories and miscellaneous items underperform.

This points to Electronics and Fitness as high-margin categories where deeper product range and upselling can enhance returns.

5. Spend Trends Over Time
(Visualizations: SpendbyDayYear.png, SpendbyDayMonth.png)

Temporal analysis uncovers seasonality and promotional opportunities:

Spend spikes occur in mid-year and holiday seasons, suggesting sales events or campaigns during these periods are effective.

Daily patterns indicate weekends and specific mid-month days often see elevated spend, possibly linked to pay cycles or marketing pushes.

Understanding these timing patterns can help optimize inventory, staffing, and promotions around seasonal peaks and high-traffic days.

Conclusion
These visualizations support strategic decision-making by identifying:

High-value demographics: 25–44 age group, females for frequency, and males for value.

Strong regions: Central and West, with growth potential in North and East.

Best-performing categories: Electronics and Fitness.

Timely engagement: Mid-year and holiday periods with weekly spend peaks.

Future strategies should emphasize personalized campaigns, region-specific promotions, and category-focused merchandising to drive growth and retain top customer segments.


Section 6. Suggested Business Action
Section 7. Challenges
Section 8. Ethical Considerations
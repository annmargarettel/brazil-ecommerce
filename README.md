# Brazil E-Commerce Analytics

An analytics pipeline for the Brazilian Olist e-commerce dataset using DuckDB, Python, and Jupyter notebooks. The project transforms raw CSV data through Bronze, Silver, and Gold layers and exports dashboard-ready datasets for Tableau.

## Architecture

```text
Raw CSV files
    ↓
Bronze layer
    ↓
Silver layer
    ↓
Gold layer
    ↓
Dashboard CSV files
    ↓
Tableau
```

## Project Structure

```text
.
├── .github/
│   ├── label.yml
│   └── workflows/
│       ├── ci.yml
│       └── label.yml
├── notebooks/
│   ├── 01_bronze.ipynb
│   ├── 02_silver.ipynb
│   └── 03_gold.ipynb
├── outputs/
│   ├── gold_dashboard/
│   ├── olist_e-commerce.pdf
│   └── olist_e-commerce.twb
├── scripts/
│   ├── run_query.py
│   └── test.py
├── tests/
│   ├── fixtures/
│   │   └── orders.csv
│   └── test_pipeline.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Technologies

- Python 3.11
- DuckDB
- Pandas
- Jupyter Notebook
- Pytest
- Ruff
- GitHub Actions
- Tableau

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/annmargarettel/brazil-ecommerce.git
   cd brazil-ecommerce
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
   *On Windows:*
   ```powershell
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Raw Data

The raw Olist dataset is not included in the repository. Create the following directory:

```bash
mkdir -p data/raw
```

Place the following CSV files in `data/raw/`:

```text
olist_closed_deals_dataset.csv
olist_customers_dataset.csv
olist_geolocation_dataset.csv
olist_marketing_qualified_leads_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv
```

> **Note:** The raw dataset can be obtained from the **Brazilian E-Commerce Public Dataset by Olist** on Kaggle.

## Running the Data Pipeline

Run the notebooks in the following order:

```text
01_bronze.ipynb
02_silver.ipynb
03_gold.ipynb
```

Start Jupyter from the repository root:

```bash
jupyter lab
```

Open the notebooks from the `notebooks/` directory and execute all cells in order.

### Bronze Layer
`01_bronze.ipynb`:
- Reads the raw CSV files from `data/raw/`
- Creates the DuckDB database
- Loads the raw datasets into base tables

### Silver Layer
`02_silver.ipynb`:
- Reads the Bronze tables
- Standardizes timestamps
- Rounds monetary values
- Creates cleaned `silver_*` tables

### Gold Layer
`03_gold.ipynb`:
- Reads the Silver tables
- Creates business-level analytical tables
- Calculates sales, payments, reviews, customers, sellers, leads, and product metrics
- Exports dashboard tables to `outputs/gold_dashboard/`

### Running Notebooks from the Command Line

From the repository root:

```bash
jupyter nbconvert \
  --execute \
  --inplace \
  --ExecutePreprocessor.timeout=-1 \
  notebooks/01_bronze.ipynb

jupyter nbconvert \
  --execute \
  --inplace \
  --ExecutePreprocessor.timeout=-1 \
  notebooks/02_silver.ipynb

jupyter nbconvert \
  --execute \
  --inplace \
  --ExecutePreprocessor.timeout=-1 \
  notebooks/03_gold.ipynb
```

## Output Tables

The Gold layer exports dashboard-ready CSV files, including:
- Monthly sales
- Peak sales month
- Credit card payment volume
- Product orders
- Closed deals
- Sellers by city and state
- Customers by state
- City cancellation rates
- Leads by origin
- Review scores
- High-value orders
- Payment methods
- Electronics product weight

The files are saved in:
```text
outputs/gold_dashboard/
```

## Tableau

The Tableau workbook and PDF are available in:
```text
outputs/olist_e-commerce.twb
outputs/olist_e-commerce.pdf
```

The Tableau dashboards use the exported Gold-layer CSV files. After rerunning the Gold notebook, refresh the Tableau data sources to load updated results.

## Testing and Code Quality

1. **Run Ruff:**
   ```bash
   ruff check scripts tests
   ```

2. **Compile Python files:**
   ```bash
   python -m compileall scripts tests
   ```

3. **Run tests:**
   ```bash
   pytest -q
   ```

4. **Validate notebook JSON:**
   ```bash
   python - <<'PY'
   import json
   from pathlib import Path
   
   for path in Path("notebooks").glob("*.ipynb"):
       json.loads(path.read_text())
       print(f"Valid notebook: {path}")
   PY
   ```

## Continuous Integration

GitHub Actions runs on pull requests targeting `main` and on pushes to `main`.

The CI workflow:
1. Installs Python 3.11
2. Installs dependencies
3. Runs Ruff
4. Compiles Python files
5. Runs Pytest
6. Validates notebook files

The workflow is located at:
```text
.github/workflows/ci.yml
```

Pull requests are also automatically labeled based on the files they modify. Label configuration is located at:
```text
.github/label.yml
.github/workflows/label.yml
```

## DuckDB and Databricks Migration

DuckDB is used for local development, testing, and analytical exploration.

The planned production architecture is:

```text
Cloud storage
    ↓
Databricks Bronze Delta tables
    ↓
Databricks Silver Delta tables
    ↓
Databricks Gold Delta tables
    ↓
Databricks SQL Warehouse
    ↓
Tableau
```

DuckDB can continue to be used locally while Databricks handles production-scale processing. Tableau should connect to the Databricks SQL Warehouse for production dashboards, while the exported CSV files remain useful for local development and testing.

## Development Workflow

1. Create a feature branch.
2. Make changes to notebooks, scripts, tests, or workflows.
3. Run the local quality checks.
4. Push the branch to GitHub.
5. Open a pull request against `main`.
6. Wait for GitHub Actions to complete.
7. Request an approval from a reviewer with write access.
8. Merge only after required checks pass and the pull request is approved.

import duckdb

con = duckdb.connect()
result = con.execute("""
    SELECT COUNT(*) AS n_orders
    FROM read_csv_auto('data/raw/olist_customers_dataset.csv')
""").fetchdf()

print(result)
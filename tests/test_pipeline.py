# tests/test_pipeline.py
import duckdb

def test_orders_fixture():
    con = duckdb.connect()
    result = con.execute(
        "SELECT COUNT(*) FROM read_csv_auto('tests/fixtures/orders.csv')"
    ).fetchone()[0]
    assert result > 0

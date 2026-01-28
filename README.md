How to Run:
# Terminal 1: Start Mock API
cd /app/adpo-demo-pipeline && python mock_api.py

# Terminal 2: Start Dagster
cd /app/adpo-demo-pipeline && dagster dev -f orchestration/dagster_defs.py

# Open http://localhost:3000 → Click "Materialize All"
Query Data After Run:
import duckdb
conn = duckdb.connect("warehouse.duckdb")
conn.execute("SELECT * FROM orders_validated").fetchdf()
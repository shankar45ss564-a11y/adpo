# import sys
# sys.path.insert(0, '/workspaces/adpo/adpo-demo-pipeline')

# from dagster import materialize
# from orchestration.dagster_defs import orders_raw, orders_transformed, orders_validated
# from dagster_duckdb_pandas import DuckDBPandasIOManager

# # Make sure mock_api.py is running first!
# result = materialize(
#     assets=[orders_raw, orders_transformed, orders_validated],
#     resources={"io_manager": DuckDBPandasIOManager(database="warehouse.duckdb")}
# )

# # Now query works
# import duckdb
# conn = duckdb.connect("warehouse.duckdb")
# print(conn.execute("SELECT * FROM orders_validated").fetchdf())

# import sys
# sys.path.insert(0, '/workspaces/adpo/adpo-demo-pipeline')

# from dagster import materialize
# from orchestration.dagster_defs import orders_raw, orders_transformed, orders_validated
# from dagster_duckdb_pandas import DuckDBPandasIOManager

# # Materialize assets
# result = materialize(
#     assets=[orders_raw, orders_transformed, orders_validated],
#     resources={"io_manager": DuckDBPandasIOManager(database="warehouse.duckdb")}
# )

# Query in a separate scope to avoid variable name conflict
import duckdb
conn = duckdb.connect("warehouse.duckdb")
print(conn.execute("SELECT * FROM information_schema.tables").fetchdf())
print(conn.execute("SELECT * FROM warehouse.public.orders_raw").fetchdf())  # Use schema prefix
# conn.close()

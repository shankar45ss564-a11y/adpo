"""
Dagster pipeline definitions for the ADPO demo pipeline.
Orchestrates ingestion, transformation, and quality checks for orders data.
Data is automatically persisted to DuckDB via the I/O Manager.
"""

from dagster import (
    asset,
    define_asset_job,
    in_process_executor,
)
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.fetch_orders import fetch_orders
from observability.event_emitter import emit_event


@asset
def orders_raw() -> pd.DataFrame:
    """
    Fetch raw orders data from the API.
    Returns DataFrame - automatically saved to DuckDB table 'orders_raw'.
    """
    emit_event("ASSET_START", "orders_pipeline", "orders_raw", "STARTED")
    try:
        orders = fetch_orders()
        df = pd.DataFrame(orders)
        emit_event("ASSET_SUCCESS", "orders_pipeline", "orders_raw", "SUCCESS", 
                   {"rows": len(df)})
        return df
    except Exception as e:
        emit_event("ASSET_FAILED", "orders_pipeline", "orders_raw", "FAILED", {"error": str(e)})
        raise


@asset
def orders_transformed(orders_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Transform raw orders data.
    Receives DataFrame from DuckDB, returns transformed DataFrame.
    """
    emit_event("ASSET_START", "orders_pipeline", "orders_transformed", "STARTED")
    try:
        df = orders_raw.copy()
        
        # Ensure proper data types
        df['order_id'] = df['order_id'].astype(int)
        
        # Handle customer_id - use 0 as default if not present
        # if 'customer_id' in df.columns:
        #     df['customer_id'] = df['customer_id'].astype(int)
        # else:
        #     df['customer_id'] = 0
        
        # Handle customer_id - require it to be present and non-null
        if 'customer_id' not in df.columns:
            raise ValueError("customer_id column is required")
        
        df['customer_id'] = df['customer_id'].astype(int)
        
        # Check for null customer_id values and raise error
        if df['customer_id'].isna().any():
            raise ValueError("customer_id contains null values")

        # Keep additional columns if present (amount, status, etc.)
        emit_event("ASSET_SUCCESS", "orders_pipeline", "orders_transformed", "SUCCESS",
                   {"rows": len(df), "columns": list(df.columns)})
        return df
    except Exception as e:
        emit_event("ASSET_FAILED", "orders_pipeline", "orders_transformed", "FAILED", {"error": str(e)})
        raise


@asset
def orders_validated(orders_transformed: pd.DataFrame) -> pd.DataFrame:
    """
    Validate transformed orders data against quality expectations.
    Returns validated DataFrame - saved to DuckDB table 'orders_validated'.
    """
    emit_event("ASSET_START", "orders_pipeline", "orders_validated", "STARTED")
    try:
        df = orders_transformed.copy()
        
        # Validation checks
        assert 'order_id' in df.columns, "Missing required column: order_id"
        assert 'customer_id' in df.columns, "Missing required column: customer_id"
        assert df['order_id'].dtype in ['int64', 'int32', int], "order_id must be integer"
        assert df['customer_id'].dtype in ['int64', 'int32', int], "customer_id must be integer"
        assert not df['order_id'].isna().any(), "order_id contains null values"
        
        emit_event("ASSET_SUCCESS", "orders_pipeline", "orders_validated", "SUCCESS",
                   {"rows": len(df), "validation": "passed"})
        return df
    except Exception as e:
        emit_event("ASSET_FAILED", "orders_pipeline", "orders_validated", "FAILED", {"error": str(e)})
        raise


# Define a job that includes all assets
orders_pipeline_job = define_asset_job(
    "orders_pipeline_job",
    selection="*",
    executor_def=in_process_executor,
)




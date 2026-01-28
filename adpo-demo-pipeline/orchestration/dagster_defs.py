"""
Dagster pipeline definitions for the ADPO demo pipeline.
Orchestrates ingestion, transformation, and quality checks for orders data.
"""

from dagster import (
    asset,
    define_asset_job,
    in_process_executor,
)
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.fetch_orders import fetch_orders
from observability.event_emitter import emit_event


@asset
def orders_raw():
    """
    Fetch raw orders data from the API.
    """
    emit_event("ASSET_START", "orders_pipeline", "orders_raw", "STARTED")
    try:
        orders = fetch_orders()
        emit_event("ASSET_SUCCESS", "orders_pipeline", "orders_raw", "SUCCESS")
        return orders
    except Exception as e:
        emit_event("ASSET_FAILED", "orders_pipeline", "orders_raw", "FAILED", {"error": str(e)})
        raise


@asset
def orders_transformed(orders_raw):
    """
    Transform raw orders data.
    """
    emit_event("ASSET_START", "orders_pipeline", "orders_transformed", "STARTED")
    try:
        # Ensure we have a list of dicts
        if isinstance(orders_raw, str):
            import json
            orders_raw = json.loads(orders_raw)
        
        # Transform: ensure proper data types and add any computed fields
        transformed_orders = []
        for order in orders_raw:
            transformed_order = {
                'order_id': int(order.get('order_id', 0)),
                'customer_id': int(order.get('customer_id', 0))
            }
            transformed_orders.append(transformed_order)
        
        emit_event("ASSET_SUCCESS", "orders_pipeline", "orders_transformed", "SUCCESS")
        return transformed_orders
    except Exception as e:
        emit_event("ASSET_FAILED", "orders_pipeline", "orders_transformed", "FAILED", {"error": str(e)})
        raise


@asset
def orders_validated(orders_transformed):
    """
    Validate transformed orders data against quality expectations.
    """
    emit_event("ASSET_START", "orders_pipeline", "orders_validated", "STARTED")
    try:
        # Basic validation
        if not isinstance(orders_transformed, list):
            raise ValueError("orders_transformed must be a list")
        
        for record in orders_transformed:
            if 'order_id' not in record or 'customer_id' not in record:
                raise ValueError("Missing required fields: order_id, customer_id")
            if not isinstance(record['order_id'], int) or not isinstance(record['customer_id'], int):
                raise ValueError("order_id and customer_id must be integers")
        
        emit_event("ASSET_SUCCESS", "orders_pipeline", "orders_validated", "SUCCESS")
        return orders_transformed
    except Exception as e:
        emit_event("ASSET_FAILED", "orders_pipeline", "orders_validated", "FAILED", {"error": str(e)})
        raise


# Define a job that includes all assets
orders_pipeline_job = define_asset_job(
    "orders_pipeline_job",
    selection="*",
    executor_def=in_process_executor,
)

"""
ADPO Demo Pipeline - Data ingestion, transformation, and quality checks using Dagster.
"""

from dagster import Definitions, load_assets_from_modules
import sys
import os

# Add the package directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestration import dagster_defs

# Load all assets from the dagster_defs module
assets = load_assets_from_modules([dagster_defs])

# Create definitions for Dagster to discover
defs = Definitions(
    assets=assets,
    jobs=[dagster_defs.orders_pipeline_job],
)

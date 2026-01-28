# ADPO Dagster Pipeline - Quick Start Guide

## Prerequisites
All Airflow code has been removed and the pipeline is now fully configured for Dagster.

### Assets Defined
- ✅ `orders_raw` - Fetches orders from API
- ✅ `orders_transformed` - Transforms and normalizes data
- ✅ `orders_validated` - Validates data quality

## Setup Instructions

### 1. Install Dependencies
```bash
cd /workspaces/adpo/adpo-demo-pipeline
pip install -r requirements.txt
```

### 2. Start the Mock API (in one terminal)
```bash
cd /workspaces/adpo/adpo-demo-pipeline
python mock_api.py
```
This starts a Flask server on `http://localhost:5000` with the `/orders` endpoint.

### 3. Run Dagster (in another terminal)
```bash
cd /workspaces/adpo/adpo-demo-pipeline
dagster dev -f orchestration/dagster_defs.py
```

### 4. Access Dagster UI
- Open browser to `http://localhost:3000`
- Navigate to the "Runs" tab
- Click "Materialize All" or select individual assets to run
- Watch the pipeline execute with all three assets

## Testing Without Running the Server
To test the assets without starting the API:

```python
import sys
sys.path.insert(0, '/workspaces/adpo/adpo-demo-pipeline')

# Patch fetch_orders with mock data
from ingestion import fetch_orders as fetch_module
fetch_module.fetch_orders = lambda: [
    {"order_id": 1, "customer_id": 101},
    {"order_id": 2, "customer_id": 102}
]

# Import and run assets
from orchestration.dagster_defs import orders_raw, orders_transformed, orders_validated

orders_raw()
orders_transformed(...)
orders_validated(...)
```

## What Was Changed

### Removed
- ❌ `apache-airflow` from requirements.txt
- ❌ `/orchestration/airflow_dags/` directory

### Added/Updated
- ✅ `orchestration/dagster_defs.py` - Asset definitions
- ✅ Updated API endpoint: `http://mock-api/orders` → `http://localhost:5000/orders`
- ✅ Proper Definitions export in root `__init__.py`
- ✅ Event emissions now use `orders_pipeline` ID

## Asset Dependencies
```
orders_raw
    ↓
orders_transformed  
    ↓
orders_validated
```

## Troubleshooting

### "All materializations failed"
**Solution**: Start the mock API server first!
```bash
python mock_api.py  # Must be running before materialization
```

### Import errors
**Solution**: Ensure PYTHONPATH includes the pipeline directory:
```bash
cd /workspaces/adpo/adpo-demo-pipeline
dagster dev -f orchestration/dagster_defs.py
```

### Assets not showing in Dagster UI
**Solution**: Check that `__init__.py` properly exports definitions and restart `dagster dev`

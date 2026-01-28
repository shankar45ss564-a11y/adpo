import random, time, requests
from observability.event_emitter import emit_event

def fetch_orders():
    emit_event("TASK_START", "orders_daily", "ingest_orders", "STARTED")

    # Failure injection
    if random.random() < 0.2:
        time.sleep(40)  # timeout simulation

    response = requests.get("http://mock-api/orders", timeout=30)

    if response.status_code != 200:
        emit_event(
            "TASK_FAILED",
            "orders_daily",
            "ingest_orders",
            "FAILED",
            {"http_code": response.status_code}
        )
        raise Exception("API Failure")

    emit_event("TASK_SUCCESS", "orders_daily", "ingest_orders", "SUCCESS")

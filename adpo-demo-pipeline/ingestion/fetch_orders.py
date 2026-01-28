import random, time, requests
from observability.event_emitter import emit_event

def fetch_orders():
    emit_event("TASK_START", "orders_pipeline", "fetch_orders", "STARTED")

    # Failure injection (simulates long timeout)
    if random.random() < 0.2:
        time.sleep(40)

    response = requests.get("http://localhost:5000/orders", timeout=30)

    # HTTP-level failure
    if response.status_code != 200:
        emit_event(
            "TASK_FAILED",
            "orders_pipeline",
            "fetch_orders",
            "FAILED",
            {"http_code": response.status_code}
        )
        raise Exception("API Failure: http {}".format(response.status_code))

    # Validate payload shape — expect a list of order dicts
    data = response.json()
    if not isinstance(data, list):
        emit_event(
            "TASK_FAILED",
            "orders_pipeline",
            "fetch_orders",
            "FAILED",
            {"error": "unexpected payload", "payload_type": type(data).__name__}
        )
        raise ValueError("Unexpected payload from orders API: expected list")

    # Ensure required fields are present
    for idx, item in enumerate(data):
        if not isinstance(item, dict) or 'customer_id' not in item:
            emit_event(
                "TASK_FAILED",
                "orders_pipeline",
                "fetch_orders",
                "FAILED",
                {"error": "missing customer_id", "index": idx}
            )
            raise ValueError(f"Order at index {idx} missing required field 'customer_id'")

    emit_event("TASK_SUCCESS", "orders_pipeline", "fetch_orders", "SUCCESS")
    return data

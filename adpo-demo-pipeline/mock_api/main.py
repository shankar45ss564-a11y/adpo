from fastapi import FastAPI
from data import ORDERS
import random
import time

app = FastAPI()

@app.get("/orders")
def get_orders():
    # Simulate latency
    time.sleep(random.uniform(0.2, 1.5))

    # Simulate occasional API failure
    if random.random() < 0.15:
        return {"error": "Upstream service unavailable"}

    return ORDERS

from fastapi import FastAPI, HTTPException
from data import ORDERS
import random
import time

app = FastAPI()


@app.get("/orders")
def get_orders():
    # Simulate latency
    time.sleep(random.uniform(0.2, 1.5))

    # Simulate occasional API failure — return proper HTTP error
    if random.random() < 0.15:
        raise HTTPException(status_code=503, detail="Upstream service unavailable")

    return ORDERS

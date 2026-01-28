from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route("/orders")
def orders():
    if random.random() < 0.2:
        return "Rate limited", 429

    return jsonify([
        {"order_id": 1, "amount": 250, "status": "CREATED", "customer_id": 101},
    {"order_id": 2, "amount": 900, "status": "SHIPPED", "customer_id": 102},
    {"order_id": 3, "amount": 120, "status": "CREATED", "customer_id": 103},
    {"order_id": 4, "amount": 560, "status": "CANCELLED", "customer_id": 104},
    ])

app.run(port=5000)

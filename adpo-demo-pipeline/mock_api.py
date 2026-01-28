from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route("/orders")
def orders():
    if random.random() < 0.2:
        return "Rate limited", 429

    return jsonify([
        {"order_id": 1, "amount": 250, "status": "CREATED"},
    {"order_id": 2, "amount": 900, "status": "SHIPPED"},
    {"order_id": 3, "amount": 120, "status": "CREATED"},
    {"order_id": 4, "amount": 560, "status": "CANCELLED"},
    ])

app.run(port=5000)

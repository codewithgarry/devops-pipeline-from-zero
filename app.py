import os

from flask import Flask, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

app = Flask(__name__)

MENU = {"chai": 20, "coffee": 40, "samosa": 15}
SHOP = os.environ.get("SHOP_NAME", "Chai shop")
GST = float(os.environ.get("GST_RATE", "0.05"))
VERSION = os.environ.get("APP_VERSION", "dev")
ORDERS = Counter("chai_orders_total", "Orders placed", ["item"])


def bill(item, qty):
    price = MENU[item] * qty
    gst = round(price * GST, 2)
    return {"item": item, "qty": qty, "price": price, "gst": gst, "total": round(price + gst, 2)}


@app.get("/")
def home():
    return f"{SHOP} is open: {", ".join(MENU)}\n"


@app.get("/menu")
def menu():
    return jsonify(MENU)


@app.post("/order")
def order():
    data = request.get_json(force=True)
    item, qty = data.get("item"), int(data.get("qty", 1))
    if item not in MENU:
        return jsonify(error=f"we do not sell {item}"), 404
    ORDERS.labels(item).inc(qty)
    return jsonify(bill(item, qty))


@app.get("/health")
def health():
    return {"status": "ok", "version": VERSION}


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

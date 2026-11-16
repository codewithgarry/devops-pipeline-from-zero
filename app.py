import os

from flask import Flask, jsonify, request

app = Flask(__name__)

MENU = {"chai": 20, "coffee": 40, "samosa": 15}
SHOP = os.environ.get("SHOP_NAME", "Chai shop")
GST = float(os.environ.get("GST_RATE", "0.05"))
VERSION = os.environ.get("APP_VERSION", "dev")


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
    return jsonify(bill(item, qty))


@app.get("/health")
def health():
    return {"status": "ok", "version": VERSION}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

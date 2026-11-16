from app import app, bill


def test_bill_adds_gst():
    assert bill("chai", 2) == {"item": "chai", "qty": 2, "price": 40, "gst": 2.0, "total": 42.0}


def test_order():
    r = app.test_client().post("/order", json={"item": "samosa", "qty": 3})
    assert r.status_code == 200
    assert r.get_json()["total"] == 47.25


def test_unknown_item():
    r = app.test_client().post("/order", json={"item": "pizza"})
    assert r.status_code == 404


def test_health():
    assert app.test_client().get("/health").get_json()["status"] == "ok"
def test_metrics_count_orders():
    app.test_client().post("/order", json={"item": "chai", "qty": 2})
    assert b'chai_orders_total{item="chai"}' in app.test_client().get("/metrics").data

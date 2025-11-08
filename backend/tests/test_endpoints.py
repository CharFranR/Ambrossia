import time
import requests

BASE_URL = "http://localhost:8000"


def _post(path: str, json=None):
    return requests.post(f"{BASE_URL}{path}", json=json)


def _get(path: str):
    return requests.get(f"{BASE_URL}{path}")


def _put(path: str, json=None):
    return requests.put(f"{BASE_URL}{path}", json=json)


def _wait_server(max_wait_s=10):
    start = time.time()
    while time.time() - start < max_wait_s:
        try:
            # hit a cheap endpoint (404 expected means server is up)
            r = requests.get(f"{BASE_URL}/__health__/")
            if r.status_code in (200, 404):
                return True
        except Exception:
            time.sleep(0.2)
    return False


def add_table():
    resp = _post("/tables/")
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data and "status" in data
    return data["id"]


def add_product(name="Test", price=10):
    resp = _post("/product/", json={"name": name, "price": price})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == name and data["price"] == price
    return data["id"]


def add_order(table_id: int, product_id: int):
    resp = _post(f"/tables/{table_id}/orders/", json={"product": product_id})
    assert resp.status_code == 200
    data = resp.json()
    assert data["table"] == table_id and data["product"] == product_id
    return data["id"]


def create_bill(table_id: int):
    resp = _post(f"/tables/{table_id}/bills/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "notPayed"
    # Validar campos nuevos
    for field in ["amount", "IVA", "discount", "total"]:
        assert field in data, f"Falta campo {field} en la respuesta de bill"
        assert isinstance(data[field], (int, float)), f"{field} debe ser numérico"
    return data["id"]


def update_bill_status(bill_id: int, status: str):
    resp = _put(f"/bills/{bill_id}/status/", json={"status": status})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == status


    # Ensure server is up (when running under Docker)
    assert _wait_server(), "API server is not reachable on http://localhost:8000"

    # 1) Create a table
    table_id = add_table()

    # 2) Check table status
    resp = _get(f"/tables/{table_id}/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "available"

    # 3) Update table status
    resp = _put(f"/tables/{table_id}/", json={"new_status": "reserved"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "reserved"

    # 4) Create a product and list products
    prod_id = add_product(name="Pizza", price=25)
    resp = _get("/Products/All")
    assert resp.status_code == 200
    assert any(p["id"] == prod_id for p in resp.json())

    # 5) Create an order for the table
    add_order(table_id, prod_id)

    # 6) Create a bill for that table
    bill_id = create_bill(table_id)


    # 7) Not payed bills should include ours y tener los campos nuevos
    resp = _get("/bills/not-payed/")
    assert resp.status_code == 200
    found = False
    for b in resp.json():
        if b["id"] == bill_id:
            found = True
            for field in ["amount", "IVA", "discount", "total"]:
                assert field in b, f"Falta campo {field} en bill listada"
                assert isinstance(b[field], (int, float)), f"{field} debe ser numérico"
    assert found, "La bill creada no aparece en la lista de not-payed"

    # 8) Update bill status to payed
    update_bill_status(bill_id, "payed")


    # 9) Payed bills should include ours y tener los campos nuevos
    resp = _get("/bills/payed/")
    assert resp.status_code == 200
    found = False
    for b in resp.json():
        if b["id"] == bill_id:
            found = True
            for field in ["amount", "IVA", "discount", "total"]:
                assert field in b, f"Falta campo {field} en bill listada"
                assert isinstance(b[field], (int, float)), f"{field} debe ser numérico"
    assert found, "La bill pagada no aparece en la lista de payed"

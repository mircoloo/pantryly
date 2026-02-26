from app.core.database import get_db
from app.main import app

def test_create_product_correct(client):
    response = client.post("/v1/products", json={
        "name": "Test Product",
        "barcode": "123456789012",
        "expiration_date": "2025-12-31"
    })

    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"

def test_create_same_name_product_exists(client):
    response_1 = client.post("/v1/products", json={
        "name": "Test Product",
        "barcode": "123",
        "expiration_date": "2025-12-31"
    })
    response_2 = client.post("/v1/products", json={
        "name": "Test Product",
        "barcode": "1234",
        "expiration_date": "2025-12-31"
    })

    assert response_2.status_code == 400
    assert response_2.json()['detail'] == "Product with name Test Product already exists"
    
def test_create_same_barcode_product_exists(client):
    response_1 = client.post("/v1/products", json={
        "name": "Test Product 1",
        "barcode": "123",
        "expiration_date": "2025-12-31"
    })
    response_2 = client.post("/v1/products", json={
        "name": "Test Product 2",
        "barcode": "123",
        "expiration_date": "2025-12-31"
    })

    assert response_2.status_code == 400
    assert response_2.json()['detail'] == "Product with barcode 123 already exists"
    
def test_get_all_products(client):
    response_1 = client.post("/v1/products", json={"name": "Test Product 1","barcode": "123","expiration_date": "2025-12-31"})
    response_2 = client.post("/v1/products", json={"name": "Test Product 2","barcode": "1234","expiration_date": "2025-12-31"})
    res = client.get("/v1/products")
    assert len(res.json()) == 2
    
def test_delete_product(client):
    response_1 = client.post("/v1/products", json={"name": "Test Product 1","barcode": "123","expiration_date": "2025-12-31"})
    assert response_1.status_code == 201
    delete_response = client.delete("/v1/products/1")
    assert delete_response.status_code == 204 
    
def test_delete_product_doesnt_exists(client):
    delete_response = client.delete("/v1/products/1")
    assert delete_response.status_code == 400
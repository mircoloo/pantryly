
def test_get_all_products(client, get_test_user_id):
    client.post(
        "/v1/products",
        json={
            "name": "Test Product 1",
            "user_id": get_test_user_id,
            "barcode": "123",
            "expiration_date": "2025-12-31",
        },
    )
    client.post(
        "/v1/products",
        json={
            "name": "Test Product 2",
            "user_id": get_test_user_id,
            "barcode": "1234",
            "expiration_date": "2025-12-31",
        },
    )
    client.post(
        "/v1/products",
        json={
            "name": "Test Product 3",
            "user_id": get_test_user_id,
            "barcode": "12345",
            "expiration_date": "2025-12-31",
        },
    )
    res = client.get(f"/v1/products?user_id={get_test_user_id}")
    print(res.json())
    # Check that the responses are actually products
    for prod in res.json():
        assert prod['user_id'] and prod['name'] and prod['barcode'] and prod["expiration_date"]

    assert len(res.json()) == 3


def test_get_product_by_id_success(client, get_test_user_id):
    create_response = client.post(
        "/v1/products",
        json={
            "name": "Milk",
            "user_id": get_test_user_id,
            "barcode": "milk-001",
            "expiration_date": "2026-12-31",
        },
    )
    product_id = create_response.json()["id"]

    response = client.get(f"/v1/products/{product_id}?user_id={get_test_user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == product_id
    assert response.json()["name"] == "Milk"


def test_get_product_by_id_not_found(client, get_test_user_id):
    response = client.get(f"/v1/products/9999?user_id={get_test_user_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_get_product_by_name_success(client, get_test_user_id):
    client.post(
        "/v1/products",
        json={
            "name": "Pasta",
            "user_id": get_test_user_id,
            "barcode": "pasta-001",
            "expiration_date": "2026-12-31",
        },
    )

    response = client.get(f"/v1/products/by-name/Pasta?user_id={get_test_user_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Pasta"


def test_get_product_by_name_not_found(client, get_test_user_id):
    response = client.get(f"/v1/products/by-name/Unknown?user_id={get_test_user_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_get_product_by_barcode_success(client, get_test_user_id):
    client.post(
        "/v1/products",
        json={
            "name": "Bread",
            "user_id": get_test_user_id,
            "barcode": "bread-001",
            "expiration_date": "2026-12-31",
        },
    )

    response = client.get(
        f"/v1/products/by-barcode/bread-001?user_id={get_test_user_id}"
    )

    assert response.status_code == 200
    assert response.json()["barcode"] == "bread-001"


def test_get_product_by_barcode_not_found(client, get_test_user_id):
    response = client.get(
        f"/v1/products/by-barcode/not-existing?user_id={get_test_user_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_get_all_products_is_scoped_by_user(client):
    client.post(
        "/v1/products",
        json={
            "name": "User One Product",
            "user_id": 1,
            "barcode": "u1-001",
            "expiration_date": "2026-12-31",
        },
    )
    client.post(
        "/v1/products",
        json={
            "name": "User Two Product",
            "user_id": 2,
            "barcode": "u2-001",
            "expiration_date": "2026-12-31",
        },
    )

    user_one_response = client.get("/v1/products?user_id=1")
    user_two_response = client.get("/v1/products?user_id=2")

    assert user_one_response.status_code == 200
    assert user_two_response.status_code == 200
    assert len(user_one_response.json()) == 1
    assert len(user_two_response.json()) == 1
    assert user_one_response.json()[0]["name"] == "User One Product"
    assert user_two_response.json()[0]["name"] == "User Two Product"


def test_get_product_by_id_of_another_user_returns_not_found(client):
    create_response = client.post(
        "/v1/products",
        json={
            "name": "Private Product",
            "user_id": 1,
            "barcode": "private-001",
            "expiration_date": "2026-12-31",
        },
    )
    product_id = create_response.json()["id"]

    response = client.get(f"/v1/products/{product_id}?user_id=2")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"
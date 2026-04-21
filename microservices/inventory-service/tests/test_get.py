
def test_get_all_products(client, auth_headers):
    client.post(
        "/api/v1/products",
        json={
            "name": "Test Product 1",
            "barcode": "123",
            "expiration_date": "2025-12-31",
        },
        headers=auth_headers
    )
    client.post(
        "/api/v1/products",
        json={
            "name": "Test Product 2",
            "barcode": "1234",
            "expiration_date": "2025-12-31",
        },
        headers=auth_headers
    )
    client.post(
        "/api/v1/products",
        json={
            "name": "Test Product 3",
            "barcode": "12345",
            "expiration_date": "2025-12-31",
        },
        headers=auth_headers
    )
    res = client.get("/api/v1/products", headers=auth_headers)
    print(res.json())
    # Check that the responses are actually products
    for prod in res.json():
        assert prod['user_id'] and prod['name'] and prod['barcode'] and prod["expiration_date"]

    assert len(res.json()) == 3


def test_get_product_by_id_success(client, auth_headers):
    create_response = client.post(
        "/api/v1/products",
        json={
            "name": "Milk",
            "barcode": "milk-001",
            "expiration_date": "2026-12-31",
        },
        headers=auth_headers
    )
    product_id = create_response.json()["id"]

    response = client.get(f"/api/v1/products/{product_id}",headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["id"] == product_id
    assert response.json()["name"] == "Milk"


def test_get_product_by_id_not_found(client, auth_headers):
    response = client.get("/api/v1/products/9999", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_get_product_by_name_success(client, auth_headers):
    client.post(
        "/api/v1/products",
        json={
            "name": "Pasta",
            "barcode": "pasta-001",
            "expiration_date": "2026-12-31",
        },
        headers=auth_headers,
    )

    response = client.get("/api/v1/by-name/Pasta", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["name"] == "Pasta"


def test_get_product_by_name_not_found(client, auth_headers):
    response = client.get("/api/v1/by-name/Unknown", headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_get_product_by_barcode_success(client, auth_headers):
    client.post(
        "/api/v1/products",
        json={
            "name": "Bread",
            "barcode": "bread-001",
            "expiration_date": "2026-12-31",
        },
        headers=auth_headers,
    )

    response = client.get(
        "/api/v1/by-barcode/bread-001", headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["barcode"] == "bread-001"


def test_get_product_by_barcode_not_found(client, auth_headers):
    response = client.get(
        "/api/v1/by-barcode/not-existing",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_get_all_products_is_scoped_by_user(client, auth_headers):
    client.post(
        "/api/v1/products",
        json={
            "name": "User One Product",
            "barcode": "u1-001",
            "expiration_date": "2026-12-31",
        },
        headers=auth_headers
    )
    client.post(
        "/api/v1/products",
        json={
            "name": "User Two Product",
            "barcode": "u2-001",
            "expiration_date": "2026-12-31",
        },
        headers= {"X-User-Id": "2"}
    )

    user_one_response = client.get("/api/v1/products",headers=auth_headers)
    user_two_response = client.get("/api/v1/products", headers={"X-User-Id": "2"})

    assert user_one_response.status_code == 200
    assert user_two_response.status_code == 200
    assert len(user_one_response.json()) == 1
    assert len(user_two_response.json()) == 1
    assert user_one_response.json()[0]["name"] == "User One Product"
    assert user_two_response.json()[0]["name"] == "User Two Product"


def test_get_product_by_id_of_another_user_returns_not_found(client, auth_headers):
    create_response = client.post(
        "/api/v1/products",
        json={
            "name": "Private Product",
            "barcode": "private-001",
            "expiration_date": "2026-12-31",
        },
        headers=auth_headers
    )
    product_id = create_response.json()["id"]

    response = client.get(f"/api/v1/products/{product_id}", headers={"X-User-Id": "2"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"
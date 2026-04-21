def test_create_product_correct(client, auth_headers):
    response = client.post(
        "/api/v1/products",
        json={
            "name": "Test Product",
            "barcode": "123456789012",
            "expiration_date": "2025-12-31",
        },
        headers=auth_headers
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"


def test_create_same_name_product_exists(client, auth_headers):
    client.post(
        "/api/v1/products",
        json={
            "name": "Test Product",
            "barcode": "123",
            "expiration_date": "2025-12-31",
        },
        headers=auth_headers
    )
    response_2 = client.post(
        "/api/v1/products",
        json={
            "name": "Test Product",
            "barcode": "1234",
            "expiration_date": "2025-12-31",
        },
        headers=auth_headers,
    )

    assert response_2.status_code == 400
    assert (
        response_2.json()["detail"] == "Product with name Test Product already exists"
    )


def test_create_same_barcode_product_exists(client, auth_headers):
    client.post(
        "/api/v1/products",
        json={
            "name": "Test Product 1",
            "barcode": "123",
            "expiration_date": "2025-12-31",
        },
        headers=auth_headers,
    )
    response_2 = client.post(
        "/api/v1/products",
        json={
            "name": "Test Product 2",
            "barcode": "123",
            "expiration_date": "2025-12-31",
        },
        headers=auth_headers,
    )

    assert response_2.status_code == 400
    assert response_2.json()["detail"] == "Product with barcode 123 already exists"

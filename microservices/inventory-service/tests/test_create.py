def test_create_product_correct(client):
    response = client.post(
        "/v1/products",
        json={
            "name": "Test Product",
            "user_id": 1,
            "barcode": "123456789012",
            "expiration_date": "2025-12-31",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"


def test_create_same_name_product_exists(client, get_test_user_id):
    client.post(
        "/v1/products",
        json={
            "name": "Test Product",
            "user_id": get_test_user_id,
            "barcode": "123",
            "expiration_date": "2025-12-31",
        },
    )
    response_2 = client.post(
        "/v1/products",
        json={
            "name": "Test Product",
            "user_id": get_test_user_id,
            "barcode": "1234",
            "expiration_date": "2025-12-31",
        },
    )

    assert response_2.status_code == 400
    assert (
        response_2.json()["detail"] == "Product with name Test Product already exists"
    )


def test_create_same_barcode_product_exists(client, get_test_user_id):
    client.post(
        "/v1/products",
        json={
            "name": "Test Product 1",
            "user_id": get_test_user_id,
            "barcode": "123",
            "expiration_date": "2025-12-31",
        },
    )
    response_2 = client.post(
        "/v1/products",
        json={
            "name": "Test Product 2",
            "user_id": get_test_user_id,
            "barcode": "123",
            "expiration_date": "2025-12-31",
        },
    )

    assert response_2.status_code == 400
    assert response_2.json()["detail"] == "Product with barcode 123 already exists"

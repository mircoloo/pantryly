def test_create_product_missing_user_id_returns_422(client):
    response = client.post(
        "/v1/products",
        json={
            "name": "No User",
            "barcode": "missing-user-001",
            "expiration_date": "2026-12-31",
        },
    )

    assert response.status_code == 422


def test_create_product_invalid_expiration_date_returns_422(client):
    response = client.post(
        "/v1/products",
        json={
            "name": "Bad Date",
            "user_id": 1,
            "barcode": "bad-date-001",
            "expiration_date": "not-a-date",
        },
    )

    assert response.status_code == 422


def test_create_product_missing_name_returns_422(client):
    response = client.post(
        "/v1/products",
        json={
            "user_id": 1,
            "barcode": "missing-name-001",
            "expiration_date": "2026-12-31",
        },
    )

    assert response.status_code == 422


def test_get_products_missing_user_id_returns_422(client):
    response = client.get("/v1/products")

    assert response.status_code == 422


def test_get_product_by_id_with_invalid_path_param_returns_422(client):
    response = client.get("/v1/products/not-an-int?user_id=1")

    assert response.status_code == 422

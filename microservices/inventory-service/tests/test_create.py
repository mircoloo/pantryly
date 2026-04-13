from fastapi import status


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

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Test Product"


def test_create_same_name_product_exists(client,get_test_user_id):
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

    assert response_2.status_code == status.HTTP_400_BAD_REQUEST
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

    assert response_2.status_code == status.HTTP_400_BAD_REQUEST
    assert response_2.json()["detail"] == "Product with barcode 123 already exists"


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
    assert len(res.json()) == 3


def test_delete_product(client, get_test_user_id):
    response_1 = client.post(
        "/v1/products",
        json={
            "name": "Test Product 1",
            "user_id": get_test_user_id,
            "barcode": "123",
            "expiration_date": "2025-12-31",
        },
    )
    assert response_1.status_code == status.HTTP_201_CREATED
    delete_response = client.delete(f"/v1/products/1?user_id={get_test_user_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_product_doesnt_exists(client, get_test_user_id):
    delete_response = client.delete(f"/v1/products/1?user_id={get_test_user_id}")
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND

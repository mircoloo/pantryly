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
    assert response_1.status_code == 201
    delete_response = client.delete(f"/v1/products/1?user_id={get_test_user_id}")
    assert delete_response.status_code == 204
    get_response = client.get(f"/v1/products/1?user_id={get_test_user_id}")
    assert get_response.status_code == 404


def test_delete_product_doesnt_exists(client, get_test_user_id):
    delete_response = client.delete(f"/v1/products/1?user_id={get_test_user_id}")
    assert delete_response.status_code == 404


def test_delete_product_of_another_user_returns_not_found(client):
    create_response = client.post(
        "/v1/products",
        json={
            "name": "Only For User One",
            "user_id": 1,
            "barcode": "only-user-1",
            "expiration_date": "2026-12-31",
        },
    )
    product_id = create_response.json()["id"]

    delete_response = client.delete(f"/v1/products/{product_id}?user_id=2")
    assert delete_response.status_code == 404

    still_exists_response = client.get(f"/v1/products/{product_id}?user_id=1")
    assert still_exists_response.status_code == 200

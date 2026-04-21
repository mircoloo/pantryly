from fastapi import status


def test_delete_product(client, auth_headers):
    response_1 = client.post(
        "/api/v1/products",
        json={
            "name": "Test Product 1",
            "barcode": "123",
            "expiration_date": "2025-12-31",
        },
        headers=auth_headers,
    )
    assert response_1.status_code == status.HTTP_201_CREATED
    delete_response = client.delete("/api/v1/products/1", headers=auth_headers)
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    get_response = client.get("/api/v1/products/1", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_product_doesnt_exists(client, auth_headers):
    delete_response = client.delete("/api/v1/products/1", headers=auth_headers)
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_product_of_another_user_returns_not_found(client, auth_headers):
    create_response = client.post(
        "/api/v1/products",
        json={
            "name": "Only For User One",
            "barcode": "only-user-1",
            "expiration_date": "2026-12-31",
        },
        headers=auth_headers,
    )
    product_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/products/{product_id}",
        headers={"X-User-Id": "2"},
    )
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND

    still_exists_response = client.get(
        f"/api/v1/products/{product_id}",
        headers=auth_headers,
    )
    assert still_exists_response.status_code == status.HTTP_200_OK

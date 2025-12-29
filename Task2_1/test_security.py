import pytest
from helpers.data_generator import DataGenerator

def test_sql_injection_in_name(api_client, unique_seller_id):
    data = {
        "sellerID": unique_seller_id,
        "name": DataGenerator.generate_sql_injection(),
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
    }
    response = api_client.post_item(data)
    assert response.status_code in [200, 400]

def test_xss_in_name(api_client, unique_seller_id):
    data = {
        "sellerID": unique_seller_id,
        "name": DataGenerator.generate_xss(),
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
    }
    response = api_client.post_item(data)
    assert response.status_code in [200, 400]

def test_security_headers(api_client):
    response = api_client.get_item_by_id(DataGenerator.generate_uuid())
    assert "Content-Type" in response.headers
    assert "application/json" in response.headers["Content-Type"]

def test_large_json_payload(api_client, unique_seller_id):
    data = {
        "sellerID": unique_seller_id,
        "name": DataGenerator.generate_long_string(10000),
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
    }
    response = api_client.post_item(data)
    assert response.status_code in [200, 400, 413]
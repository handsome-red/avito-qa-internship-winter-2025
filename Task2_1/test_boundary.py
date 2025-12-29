import pytest
from helpers.data_generator import DataGenerator

def test_boundary_sellerid_values(api_client):
    test_cases = [
        (111111, 200),
        (999999, 200),
        (100000, 200)
    ]
    
    for seller_id, expected_status in test_cases:
        data = {
            "sellerID": seller_id,
            "name": f"Тест sellerID {seller_id}",
            "price": 1000,
            "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
        }
        response = api_client.post_item(data)
        if response.status_code == 200:
            item_id = response.json()["status"].split(" - ")[1]
            api_client.delete_item(item_id)
        assert response.status_code == expected_status

def test_large_numeric_values(api_client, unique_seller_id):
    test_cases = [
        (2147483647, "MAX_INT"),
        (9223372036854775807, "MAX_BIGINT")
    ]
    
    for value, description in test_cases:
        data = {
            "sellerID": unique_seller_id,
            "name": f"Тест {description}",
            "price": value,
            "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
        }
        response = api_client.post_item(data)
        assert response.status_code in [200, 400]

def test_deep_json_nesting(api_client, unique_seller_id):
    nested_data = {"level1": {"level2": {"level3": {"level4": {"level5": "value"}}}}}
    data = {
        "sellerID": unique_seller_id,
        "name": "Глубокий JSON",
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
        "extra": nested_data
    }
    response = api_client.post_item(data)
    assert response.status_code in [200, 400]
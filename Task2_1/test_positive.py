import uuid
from helpers.data_generator import DataGenerator

def test_create_item_success(api_client, valid_item_data):
    response = api_client.post_item(valid_item_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "status" in response_data
    assert "Сохранили объявление -" in response_data["status"]

def test_create_item_with_zero_statistics(api_client, unique_seller_id):
    item_data = {
        "sellerID": unique_seller_id,
        "name": "Товар с нулевой статистикой",
        "price": 1000,
        "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
    }
    response = api_client.post_item(item_data)
    assert response.status_code == 200

def test_post_with_full_item_object(api_client, unique_seller_id):
    full_item = {
        "id": str(uuid.uuid4()),
        "sellerId": unique_seller_id,
        "name": "Тестовый товар",
        "price": 1000,
        "statistics": {
            "likes": 10,
            "viewCount": 100,
            "contacts": 5
        },
        "createdAt": "2024-01-15T10:30:00Z"
    }
    response = api_client.post_item(full_item)
    assert response.status_code == 200

def test_get_item_by_id(api_client, created_item):
    response = api_client.get_item_by_id(created_item["id"])
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) > 0

def test_get_seller_items(api_client, created_item):
    seller_id = created_item["data"]["sellerID"]
    response = api_client.get_seller_items(seller_id)
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)

def test_get_statistic_v1(api_client, created_item):
    response = api_client.get_statistic_v1(created_item["id"])
    assert response.status_code == 200
    statistics = response.json()
    assert isinstance(statistics, list)

def test_get_statistic_v2(api_client, created_item):
    response = api_client.get_statistic_v2(created_item["id"])
    assert response.status_code == 200
    statistics = response.json()
    assert isinstance(statistics, list)

def test_delete_item(api_client, created_item):
    response = api_client.delete_item(created_item["id"])
    assert response.status_code == 200

# Новые тесты

def test_create_item_with_min_values(api_client, unique_seller_id):
    data = {
        "sellerID": unique_seller_id,
        "name": "Товар с минимальными значениями",
        "price": 1,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
    }
    response = api_client.post_item(data)
    assert response.status_code == 200

def test_create_item_with_long_name(api_client, unique_seller_id):
    data = {
        "sellerID": unique_seller_id,
        "name": DataGenerator.generate_long_string(255),
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
    }
    response = api_client.post_item(data)
    assert response.status_code in [200, 400]

def test_create_item_with_special_chars_in_name(api_client, unique_seller_id):
    data = {
        "sellerID": unique_seller_id,
        "name": "Товар!@#$%^&*()_+",
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
    }
    response = api_client.post_item(data)
    assert response.status_code == 200

def test_get_item_structure(api_client, created_item):
    response = api_client.get_item_by_id(created_item["id"])
    items = response.json()
    item = items[0]
    assert isinstance(item["id"], str)
    assert isinstance(item["sellerId"], int)
    assert isinstance(item["name"], str)
    assert isinstance(item["price"], int)
    assert isinstance(item["statistics"], dict)
    assert isinstance(item["createdAt"], str)

def test_get_seller_items_empty(api_client, unique_seller_id):
    response = api_client.get_seller_items(unique_seller_id)
    assert response.status_code == 200
    assert response.json() == []

def test_get_seller_items_unique_ids(two_created_items, api_client):
    seller_id = two_created_items[0]["data"]["sellerID"]
    response = api_client.get_seller_items(seller_id)
    items = response.json()
    ids = [item["id"] for item in items]
    assert len(ids) == len(set(ids))

def test_compare_statistics_v1_v2(api_client, created_item):
    response_v1 = api_client.get_statistic_v1(created_item["id"])
    response_v2 = api_client.get_statistic_v2(created_item["id"])
    assert response_v1.status_code == 200
    assert response_v2.status_code == 200
    stats_v1 = response_v1.json()
    stats_v2 = response_v2.json()
    assert len(stats_v1) == len(stats_v2)
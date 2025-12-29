import pytest
from helpers.api_client import ApiClient
from helpers.data_generator import DataGenerator

BASE_URL = "https://qa-internship.avito.com"

@pytest.fixture
def api_client():
    return ApiClient(BASE_URL)

@pytest.fixture
def unique_seller_id():
    return DataGenerator.generate_seller_id()

@pytest.fixture
def valid_item_data(unique_seller_id):
    return DataGenerator.generate_valid_item()

@pytest.fixture
def created_item(api_client, valid_item_data):
    response = api_client.post_item(valid_item_data)
    assert response.status_code == 200
    data = response.json()
    item_id = data["status"].split(" - ")[1]
    return {"id": item_id, "data": valid_item_data}

@pytest.fixture
def two_created_items(api_client):
    seller_id = DataGenerator.generate_seller_id()
    items = []
    for i in range(2):
        data = {
            "sellerID": seller_id,
            "name": f"Тестовый товар {i+1}",
            "price": 1000 * (i + 1),
            "statistics": {"likes": (i + 1) * 10, "viewCount": (i + 1) * 100, "contacts": i + 1}
        }
        response = api_client.post_item(data)
        if response.status_code == 200:
            item_id = response.json()["status"].split(" - ")[1]
            items.append({"id": item_id, "data": data})
    yield items
    for item in items:
        api_client.delete_item(item["id"])

@pytest.fixture
def deleted_item(api_client, created_item):
    api_client.delete_item(created_item["id"])
    return created_item["id"]
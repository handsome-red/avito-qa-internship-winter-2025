from helpers.data_generator import DataGenerator

def test_create_item_missing_sellerid(api_client):
    data = {
        "name": "Тестовый товар",
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 2, "contacts": 3}
    }
    response = api_client.post_item(data)
    assert response.status_code == 400

def test_create_item_missing_name(api_client, unique_seller_id):
    data = {
        "sellerID": unique_seller_id,
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 2, "contacts": 3}
    }
    response = api_client.post_item(data)
    assert response.status_code == 400

def test_create_item_missing_price(api_client, unique_seller_id):
    data = {
        "sellerID": unique_seller_id,
        "name": "Товар",
        "statistics": {"likes": 1, "viewCount": 2, "contacts": 3}
    }
    response = api_client.post_item(data)
    assert response.status_code == 400

def test_create_item_missing_statistics(api_client, unique_seller_id):
    data = {
        "sellerID": unique_seller_id,
        "name": "Товар",
        "price": 1000
    }
    response = api_client.post_item(data)
    assert response.status_code == 400

def test_get_nonexistent_item(api_client):
    fake_id = DataGenerator.generate_uuid()
    response = api_client.get_item_by_id(fake_id)
    assert response.status_code in [404, 400]

def test_get_statistic_nonexistent_item(api_client):
    fake_id = DataGenerator.generate_uuid()
    response = api_client.get_statistic_v1(fake_id)
    assert response.status_code in [404, 400]

def test_delete_nonexistent_item(api_client):
    fake_id = DataGenerator.generate_uuid()
    response = api_client.delete_item(fake_id)
    assert response.status_code in [404, 400]

def test_get_seller_items_invalid_sellerid(api_client):
    response = api_client.get_seller_items("invalid")
    assert response.status_code == 400

def test_create_item_invalid_statistics_structure(api_client, unique_seller_id):
    data = {
        "sellerID": unique_seller_id,
        "name": "Товар",
        "price": 1000,
        "statistics": {"wrong": "structure"}
    }
    response = api_client.post_item(data)
    assert response.status_code == 400

# Новые тесты

def test_create_item_invalid_sellerid_type(api_client):
    data = {
        "sellerID": "не число",
        "name": "Товар",
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
    }
    response = api_client.post_item(data)
    assert response.status_code == 400

def test_create_item_invalid_price_type(api_client, unique_seller_id):
    data = {
        "sellerID": unique_seller_id,
        "name": "Товар",
        "price": "не число",
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
    }
    response = api_client.post_item(data)
    assert response.status_code == 400

def test_create_item_incomplete_statistics(api_client, unique_seller_id):
    data = {
        "sellerID": unique_seller_id,
        "name": "Товар",
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 1}
    }
    response = api_client.post_item(data)
    assert response.status_code == 400

def test_get_item_invalid_id_format(api_client):
    response = api_client.get_item_by_id("не-uuid")
    assert response.status_code == 400

def test_get_item_too_long_id(api_client):
    long_id = DataGenerator.generate_long_string(100)
    response = api_client.get_item_by_id(long_id)
    assert response.status_code == 400

def test_get_item_special_chars_id(api_client):
    response = api_client.get_item_by_id("../../../etc/passwd")
    assert response.status_code == 400

def test_get_seller_items_negative_id(api_client):
    response = api_client.get_seller_items(-1)
    assert response.status_code == 400

def test_get_statistic_invalid_id(api_client):
    response = api_client.get_statistic_v1("invalid-id")
    assert response.status_code == 400

def test_delete_idempotent(api_client, created_item):
    response1 = api_client.delete_item(created_item["id"])
    assert response1.status_code == 200
    response2 = api_client.delete_item(created_item["id"])
    assert response2.status_code in [404, 400]

def test_delete_invalid_id_format(api_client):
    response = api_client.delete_item("не-uuid")
    assert response.status_code == 400

def test_delete_already_deleted(deleted_item, api_client):
    response = api_client.delete_item(deleted_item)
    assert response.status_code in [404, 400]
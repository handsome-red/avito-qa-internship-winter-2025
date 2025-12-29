from helpers.data_generator import DataGenerator

def test_create_and_retrieve_item(api_client, unique_seller_id):
    item_data = {
        "sellerID": unique_seller_id,
        "name": "Интеграционный тест",
        "price": 5000,
        "statistics": {"likes": 10, "viewCount": 50, "contacts": 3}
    }
    
    create_response = api_client.post_item(item_data)
    assert create_response.status_code == 200
    create_data = create_response.json()
    item_id = create_data["status"].split(" - ")[1]
    
    get_response = api_client.get_item_by_id(item_id)
    assert get_response.status_code == 200
    
    stat_response = api_client.get_statistic_v1(item_id)
    assert stat_response.status_code == 200
    
    seller_response = api_client.get_seller_items(unique_seller_id)
    assert seller_response.status_code == 200
    
    delete_response = api_client.delete_item(item_id)
    assert delete_response.status_code == 200
    
    final_get = api_client.get_item_by_id(item_id)
    assert final_get.status_code in [404, 400]

def test_multiple_items_for_same_seller(api_client):
    seller_id = DataGenerator.generate_seller_id()
    created_items = []
    
    for i in range(2):
        data = {
            "sellerID": seller_id,
            "name": f"Тестовый товар {i}",
            "price": 1000 + i * 500,
            "statistics": {"likes": i + 1, "viewCount": (i + 1) * 10, "contacts": i + 1}
        }
        response = api_client.post_item(data)
        if response.status_code == 200:
            item_id = response.json()["status"].split(" - ")[1]
            created_items.append(item_id)
    
    response = api_client.get_seller_items(seller_id)
    assert response.status_code == 200
    seller_items = response.json()
    
    for item_id in created_items:
        api_client.delete_item(item_id)

def test_data_integrity(api_client, unique_seller_id):
    original_data = {
        "sellerID": unique_seller_id,
        "name": "Тест целостности",
        "price": 7777,
        "statistics": {"likes": 77, "viewCount": 777, "contacts": 7}
    }
    
    create_response = api_client.post_item(original_data)
    assert create_response.status_code == 200
    item_id = create_response.json()["status"].split(" - ")[1]
    
    get_response = api_client.get_item_by_id(item_id)
    items = get_response.json()
    retrieved_item = items[0]
    
    assert retrieved_item["name"] == original_data["name"]
    assert retrieved_item["price"] == original_data["price"]
    assert retrieved_item["sellerId"] == original_data["sellerID"]
    assert retrieved_item["statistics"]["likes"] == original_data["statistics"]["likes"]
    assert retrieved_item["statistics"]["viewCount"] == original_data["statistics"]["viewCount"]
    assert retrieved_item["statistics"]["contacts"] == original_data["statistics"]["contacts"]
    
    api_client.delete_item(item_id)

def test_parallel_operations(api_client):
    seller_ids = [DataGenerator.generate_seller_id() for _ in range(2)]
    item_ids = []
    
    for seller_id in seller_ids:
        data = {
            "sellerID": seller_id,
            "name": f"Параллельный тест {seller_id}",
            "price": 1000,
            "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
        }
        response = api_client.post_item(data)
        if response.status_code == 200:
            item_id = response.json()["status"].split(" - ")[1]
            item_ids.append(item_id)
    
    for item_id in item_ids:
        stat_response = api_client.get_statistic_v1(item_id)
        assert stat_response.status_code in [200, 404]
        api_client.delete_item(item_id)
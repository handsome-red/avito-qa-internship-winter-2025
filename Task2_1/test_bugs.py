import pytest
from helpers.data_generator import DataGenerator


def test_bug_negative_price_accepted(api_client, unique_seller_id):
    data = {
        "sellerID": unique_seller_id,
        "name": "Товар с отрицательной ценой",
        "price": -100,
        "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
    }
    response = api_client.post_item(data)
    if response.status_code == 200:
        raise AssertionError("БАГ: Отрицательная цена принимается")

def test_bug_negative_statistics_accepted(api_client, unique_seller_id):
    data = {
        "sellerID": unique_seller_id,
        "name": "Товар с отрицательной статистикой",
        "price": 100,
        "statistics": {"likes": -10, "viewCount": -5, "contacts": -1}
    }
    response = api_client.post_item(data)
    if response.status_code == 200:
        print("⚠️ БАГ: API принимает отрицательные значения статистики")

def test_bug_post_response_format(api_client, valid_item_data):
    response = api_client.post_item(valid_item_data)
    assert response.status_code == 200
    data = response.json()
    if "id" in data:
        raise AssertionError("БАГ: POST возвращает полный объект вместо статуса")

def test_bug_sellerid_field_name_mismatch(api_client, created_item):
    response = api_client.get_item_by_id(created_item["id"])
    items = response.json()
    for item in items:
        if item["id"] == created_item["id"]:
            if "sellerID" in item:
                raise AssertionError("БАГ: В ответе поле sellerID вместо sellerId")

def test_bug_status_code_mismatch(api_client):
    """BUG-007: Проверка несоответствия статусов в заголовке и теле ответа"""
    fake_id = DataGenerator.generate_uuid()
    response = api_client.get_statistic_v1(fake_id)
    
    # Если статус 404, проверяем тело ответа
    if response.status_code == 404:
        data = response.json()
        # БАГ: В заголовке 404, но в теле статус 400
        if data.get('status') == '400':
            pytest.fail("БАГ: 404 статус с сообщением статуса 400 в теле ответа")
    
    # Дополнительная проверка для других endpoint-ов
    response_item = api_client.get_item_by_id(fake_id)
    if response_item.status_code == 404:
        data_item = response_item.json()
        if 'status' in data_item and data_item['status'] == '400':
            pytest.fail("БАГ: GET /api/1/item/{id} - 404 статус с сообщением статуса 400")
    
    response_delete = api_client.delete_item(fake_id)
    if response_delete.status_code == 404:
        data_delete = response_delete.json()
        if data_delete.get('status') == '500':  # Известный баг из примера
            pytest.fail("БАГ: DELETE - 404 статус с сообщением статуса 500")
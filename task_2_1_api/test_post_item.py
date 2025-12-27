import pytest
import requests

BASE_URL = 'https://qa-internship.avito.com'

def test_post_item_success():
    """ТЕСТ 1: Успешное создание товара с полными данными."""
    url = f'{BASE_URL}/api/1/item'
    
    payload = {
        "sellerID": 12345,
        "name": "СуперСмартфон X",
        "price": 99999,
        "statistics": {
            "likes": 100,
            "viewCount": 5000,
            "contacts": 30
        }
    }
    
    response = requests.post(url, json=payload)
    
    # 1. Проверка статуса (201 Created - стандарт для успешного создания)
    assert response.status_code == 201, f'Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}'
    
    # # 2. Проверка заголовка
    # assert 'application/json' in response.headers['Content-Type']
    
    # # 3. Парсинг и проверка ответа
    # response_data = response.json()
    
    # # 3.1. Проверка наличия ВСЕХ ожидаемых полей в ответе
    # expected_fields = {'id', 'sellerId', 'name', 'price', 'statistics', 'createdAt'}
    # assert expected_fields == set(response_data.keys()), 'В ответе не хватает полей или есть лишние'
    
    # # 3.2. Проверка типов данных
    # assert isinstance(response_data['id'], str) and response_data['id'], 'id должен быть непустой строкой'
    # assert isinstance(response_data['sellerId'], int)
    # assert isinstance(response_data['name'], str) and response_data['name'] == payload['name']
    # assert isinstance(response_data['price'], int) and response_data['price'] == payload['price']
    
    # # 3.3. Проверка вложенного объекта statistics
    # assert 'statistics' in response_data
    # stats = response_data['statistics']
    # assert isinstance(stats, dict)
    # assert stats['likes'] == payload['statistics']['likes']
    # assert stats['viewCount'] == payload['statistics']['viewCount']
    # assert stats['contacts'] == payload['statistics']['contacts']
    
    # # 3.4. Проверка даты (должна быть валидной строкой ISO формата)
    # try:
    #     datetime.fromisoformat(response_data['createdAt'].replace('Z', '+00:00'))
    # except ValueError:
    #     pytest.fail(f'Поле createdAt содержит невалидную дату: {response_data["createdAt"]}')
    
    # print(f'✅ Успех! Создан товар с ID: {response_data["id"]}')
    # return response_data['id']  # Возвращаем ID для возможных последующих тестов

    def test_get_item_success():
    """ТЕСТ 1: Успешное создание товара с полными данными."""
    url = f'{BASE_URL}/api/1/item'
    
    payload = {
        "sellerID": 12345,
        "name": "СуперСмартфон X",
        "price": 99999,
        "statistics": {
            "likes": 100,
            "viewCount": 5000,
            "contacts": 30
        }
    }
    
    response = requests.post(url, json=payload)
    
    # 1. Проверка статуса (201 Created - стандарт для успешного создания)
    assert response.status_code == 201, f'Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}'
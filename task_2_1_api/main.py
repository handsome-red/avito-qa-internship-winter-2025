import pytest
import requests

BASE_URL = 'https://qa-internship.avito.com'

def test_api_root_returns_200():
    """Проверяем, что корневой эндпоинт отвечает."""
    response = requests.get(f'{BASE_URL}/')
    assert response.status_code == 200
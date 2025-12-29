import random
import string
import uuid

class DataGenerator:
    @staticmethod
    def generate_seller_id():
        return random.randint(111111, 999999)
    
    @staticmethod
    def generate_item_name():
        adjectives = ["Отличный", "Новый", "Б/у", "Редкий", "Популярный", "Тестовый", "Уникальный", "Специальный"]
        items = ["Телефон", "Ноутбук", "Велосипед", "Диван", "Автомобиль", "Стол", "Стул", "Книга"]
        return f"{random.choice(adjectives)} {random.choice(items)} {random.randint(1, 1000)}"
    
    @staticmethod
    def generate_price():
        return random.randint(1, 1000000)
    
    @staticmethod
    def generate_statistics():
        return {
            "likes": random.randint(1, 1000),
            "viewCount": random.randint(1, 10000),
            "contacts": random.randint(1, 100)
        }
    
    @staticmethod
    def generate_valid_item():
        return {
            "sellerID": DataGenerator.generate_seller_id(),
            "name": DataGenerator.generate_item_name(),
            "price": DataGenerator.generate_price(),
            "statistics": DataGenerator.generate_statistics()
        }
    
    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_string(length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_long_string(length):
        return 'A' * length
    
    @staticmethod
    def generate_special_characters():
        return '!@#$%^&*()_+{}|:"<>?[];\',./`~'
    
    @staticmethod
    def generate_sql_injection():
        return "' OR '1'='1' --"
    
    @staticmethod
    def generate_xss():
        return '<script>alert("XSS")</script>'
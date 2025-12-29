import requests

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        
    def post_item(self, data):
        return requests.post(f"{self.base_url}/api/1/item", json=data, timeout=10)
    
    def get_item_by_id(self, item_id):
        return requests.get(f"{self.base_url}/api/1/item/{item_id}", timeout=10)
    
    def get_seller_items(self, seller_id):
        return requests.get(f"{self.base_url}/api/1/{seller_id}/item", timeout=10)
    
    def get_statistic_v1(self, item_id):
        return requests.get(f"{self.base_url}/api/1/statistic/{item_id}", timeout=10)
    
    def get_statistic_v2(self, item_id):
        return requests.get(f"{self.base_url}/api/2/statistic/{item_id}", timeout=10)
    
    def delete_item(self, item_id):
        return requests.delete(f"{self.base_url}/api/2/item/{item_id}", timeout=10)
import json
import uuid
from datetime import datetime
from typing import List, Optional
import os

class DatabaseHandler:
    def __init__(self):
        self.db_dir = "database"
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

        self.users_file = os.path.join(self.db_dir, "users.json")
        self.products_file = os.path.join(self.db_dir, "products.json")
        self._init_db()

    def _init_db(self):
        try:
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = []
            self._save_users()

        try:
            with open(self.products_file, 'r') as f:
                self.products = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.products = []
            self._save_products()

    def _save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4, default=str)

    def _save_products(self):
        with open(self.products_file, 'w') as f:
            json.dump(self.products, f, indent=4, default=str)

    def create_user(self, user_data: dict) -> dict:
        user_data['id'] = str(uuid.uuid4())
        user_data['created_at'] = datetime.now().isoformat()
        self.users.append(user_data)
        self._save_users()
        return user_data

    def get_user_by_email(self, email: str) -> Optional[dict]:
        return next((user for user in self.users if user['email'] == email), None)

    def get_all_users(self) -> List[dict]:
        return self.users

    def create_product(self, product_data: dict) -> dict:
        product_data['id'] = str(uuid.uuid4())
        product_data['created_at'] = datetime.now().isoformat()
        product_data['updated_at'] = datetime.now().isoformat()
        self.products.append(product_data)
        self._save_products()
        return product_data

    def get_product_by_id(self, product_id: str) -> Optional[dict]:
        return next((product for product in self.products if product['id'] == product_id), None)

    def get_all_products(self) -> List[dict]:
        return self.products

    def update_product(self, product_id: str, product_data: dict) -> Optional[dict]:
        for i, product in enumerate(self.products):
            if product['id'] == product_id:
                self.products[i].update(product_data)
                self.products[i]['updated_at'] = datetime.now().isoformat()
                self._save_products()
                return self.products[i]
        return None

    def delete_product(self, product_id: str) -> bool:
        initial_length = len(self.products)
        self.products = [p for p in self.products if p['id'] != product_id]
        if len(self.products) < initial_length:
            self._save_products()
            return True
        return False

db = DatabaseHandler()
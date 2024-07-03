from typing import Optional, List
import uuid


class Store:

    def __init__(self, name, items: Optional[List] = None):
        self.store_id = uuid.uuid4().hex
        self.name = name
        self.items = items or {}

    def add_item(self, name, price):
        self.items.append({
            'name': name,
            'price': price
        })

    def stock_price(self):
        total = 0
        for item in self.items:
            total += item.price
        return total

    @classmethod
    def franchise(cls, store):
        return cls(f"{store.name} - franchise")

    @staticmethod
    def store_details(store):
        return f"{store.name}, total stock - {store.stock_price()}"

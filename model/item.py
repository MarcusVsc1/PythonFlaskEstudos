import uuid


class Item:

    def __init__(self, name, price, store_id):
        self.item_id = uuid.uuid4().hex
        self.name = name
        self.price = price
        self.store_id = store_id

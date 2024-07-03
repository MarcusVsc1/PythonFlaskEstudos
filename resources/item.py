import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from model.item import Item
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operações sobre Itens de lojas")


@blp.route("/item/<string:item_id>")
class ItemSingle(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message=f"Item de id {item_id} não localizado.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": f"Item de id {item_id} deletado com sucesso"}
        except KeyError:
            abort(404, message=f"Item de id {item_id} não localizado.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            for key in item_data:
                setattr(item, key, item_data[key])
            return item
        except KeyError:
            abort(404, description="Item não encontrado")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return [item for item in list(items.values())]

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        if item_data["store_id"] not in stores:
            abort(404, message=f"Loja não encontrada.")
        for item in items.values():
            if item_data["name"] == item.name and item_data["store_id"] == item.store_id:
                abort(400, message=f"Item já existe na loja")
        item = Item(**item_data)
        items[item.item_id] = item
        return item



from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from model.item import Item
from schemas import PlainItemSchema, ItemUpdateSchema, ItemSchema
from db import db

blp = Blueprint("Items", __name__, description="Operações sobre Itens de lojas")


@blp.route("/item/<string:item_id>")
class ItemSingle(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        return Item.query.get_or_404(item_id)

    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": f"Item de id {item_id} deletado"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = Item.query.get(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = Item(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return Item.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = Item(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message=f"Erro ao inserir item no banco de dados")

        return item

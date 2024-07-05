from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from model.store import Store
from schemas import PlainStoreSchema, StoreSchema

blp = Blueprint("Stores", __name__, description="Operações sobre lojas")


@blp.route("/store/<string:store_id>")
class StoreSingle(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        return Store.query.get_or_404(store_id)

    def delete(self, store_id):
        store = Store.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": f"Loja de id {store_id} deletada"}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return Store.query.all()

    @blp.arguments(PlainStoreSchema)
    @blp.response(201, PlainStoreSchema)
    def post(self, store_data):
        store = Store(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message=f"Nome da loja já existe")
        except SQLAlchemyError:
            abort(500, message=f"Erro ao inserir item no banco de dados")
        return store

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from model.store import Store
from schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Operações sobre lojas")


@blp.route("/store/<string:store_id>")
class StoreSingle(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message=f"Loja de id {store_id} não localizada.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": f"Loja de id {store_id} deletada com sucesso"}
        except KeyError:
            abort(404, message=f"Loja de id {store_id} não localizada.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return [store for store in list(stores.values())]

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store.name:
                abort(400, message=f"Loja {store_data['name']} já existe")
        store = Store(**store_data)
        stores[store.store_id] = store
        return store

from marshmallow import Schema, fields


class ItemSchema(Schema):
    item_id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(Schema):
    store_id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

from marshmallow import Schema, fields, ValidationError


class ProductSchema(Schema):
    productId = fields.Int(dumpy_only=True)
    description = fields.Str()
    name = fields.Str(required=True)
    stock_quantity = fields.Int(required=True)
    vendor = fields.Str(required=True)
    price = fields.Int(required=True)

class OfficeSchema(Schema):
    office_code = fields.Int(dump_only=True)
    address = fields.Str(required=True)
    state = fields.Str(required=True)
    country = fields.Str(required=True)

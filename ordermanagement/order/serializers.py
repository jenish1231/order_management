from flask_restful import fields

product = {
    'productId': fields.Integer,
    'description': fields.String,
    'name': fields.String,
    'stock_quantity': fields.Integer,
    'vendor': fields.String,
    'price': fields.Integer
}
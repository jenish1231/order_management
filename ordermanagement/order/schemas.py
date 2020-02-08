from marshmallow import Schema, fields, validate, ValidationError, validates
from marshmallow.decorators import validates_schema
from .models import *
from flask import request
import datetime


class ProductSchema(Schema):
    product_id = fields.Int(dumpy_only=True)
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

class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    password2 = fields.String(required=True)

    @validates('email')
    def validate_email(self, data, **kwargs):
        employee = User.query.filter_by(email=data).first()
        if employee:
            raise ValidationError(f"User with {data} already exist!")
    
    @validates_schema
    def validate_password2(self, data, **kwargs):
        pw1 = data.get('password')
        pw2 = data.get('password2')
        if pw1 != pw2:
            raise ValidationError("Password and password2 donot match!", "password")
        data.pop('password2')
        return data

class EmployeeSchema(UserSchema):
    employer_id = fields.Int(dumpy_only=True)
    job_title = fields.String(required=True)
    reports_to = fields.Int()
    employees = fields.List(fields.Nested(lambda: EmployeeSchema(exclude=("employees",))))
    office = fields.Nested(OfficeSchema)

class NewEmployeeSchema(Schema):
    employer_id = fields.Int(dumpy_only=True)
    job_title = fields.String(required=True)
    email = fields.Email(required=True)
    reports_to = fields.Int(dump_only=True)
    employees = fields.List(fields.Nested(lambda: EmployeeSchema(exclude=("employees",))))
    office = fields.Nested(OfficeSchema)

    @validates('email')
    def validate_email(self, data, **kwargs):
        employee = User.query.filter_by(email=data).first()
        if employee:
            raise ValidationError(f"User with {data} already exist!")

class CustomerSchema(UserSchema):
    customer_id = fields.Int(dump_only=True)
    name = fields.String(required=True)
   

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class OrderSchema(Schema):
    order_id = fields.Int(dump_only=True)
    customer_id = fields.Int(dump_only=True)
    quantity = fields.Int(required=True)
    ordered_date = fields.DateTime(dump_only=True)
    shipped_date = fields.DateTime(dump_only=True)
    comments = fields.String()

    def __init__(self, *args, **kwargs):
        if kwargs.get('extra'):
            self.obj = kwargs.pop('extra')
        super().__init__(*args, **kwargs)

    @validates('quantity')
    def validate_quantity(self, data, **kwargs):
        qty = self.obj.stock_quantity
        if data > qty:
            raise ValidationError(f"Cannot order more than {qty} items")
        
class DeliverSchema(Schema):
    delivery_id = fields.Int(dump_only=True)
    order_id = fields.Int(dump_only=True)
    delivered_by_id = fields.Int()
    delivered_date = fields.DateTime(dump_only=True)
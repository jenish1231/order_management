from marshmallow import Schema, fields, validate, ValidationError, validates
from marshmallow.decorators import validates_schema
from .models import *


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
            raise ValidationError("User with {} already exist!".format(data))
    
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
    # email = fields.Email(required=True)
    job_title = fields.String(required=True)
    reports_to = fields.Int()
    employees = fields.List(fields.Nested(lambda: EmployeeSchema(exclude=("employees",))))
    office = fields.Nested(OfficeSchema)
    # password = fields.String(required=True)
    # password2 = fields.String(required=True)

    

class CustomerSchema(UserSchema):
    customer_id = fields.Int(dump_only=True)
    # email = fields.Email(required=True)
    name = fields.String(required=True)
    

    # @validates('email')
    # def validate_email(self, data, **kwargs):
    #     customer = User.query.filter_by(email=data).first()
    #     if customer:
    #         raise ValidationError("Customer with {} already exist!".format(data))

    # @validates_schema
    # def validate_password2(self, data, **kwargs):
    #     pw1 = data.get('password')
    #     pw2 = data.get('password2')
    #     if pw1 != pw2:
    #         raise ValidationError("Password and password2 donot match!", "password")
    #     data.pop('password2')
    #     return data

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
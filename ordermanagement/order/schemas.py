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

class EmployeeSchema(Schema):
    employer_id = fields.Int(dumpy_only=True)
    email = fields.Email(required=True)
    job_title = fields.String(required=True)
    reports_to = fields.Int()
    employees = fields.List(fields.Nested(lambda: EmployeeSchema(exclude=("employees",))))
    office = fields.Nested(OfficeSchema)

    @validates('email')
    def validate_email(self, data, **kwargs):
        employee = Employee.query.filter_by(email=data).first()
        if employee:
            raise ValidationError("Employee with {} already exist!".format(data))
        
class CustomerSchema(Schema):
    customer_id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    name = fields.String(required=True)
    password = fields.String(required=True)
    password2 = fields.String(required=True)

    @validates('email')
    def validate_email(self, data, **kwargs):
        customer = Customer.query.filter_by(email=data).first()
        if customer:
            raise ValidationError("Customer with {} already exist!".format(data))

    @validates_schema
    def validate_password2(self, data, **kwargs):
        print(data)


from marshmallow import Schema, fields


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



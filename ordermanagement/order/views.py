
from .models import *
from .schemas import *
from .helper import *
from flask import request

class EmployeeListResource(ListResource):
    model = Employee
    schema = EmployeeSchema

class AddEmployeeToOfficeResource(GetObject, Resource):
    model = Office

    def post(self, id):
        obj = self.get_object(id)
        json_data = request.get_json()

        try:
            employee_data = EmployeeSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 400

        employee = Employee(**employee_data)
        employee.office_id = obj.office_code
        db.session.add(employee)
        db.session.commit()
        
        return EmployeeSchema().dump(employee)

        

class OfficeCreateResource(CreateResource, ListResource):
    model = Office
    schema = OfficeSchema

class ProductCreateResource(CreateResource, ListResource):
    model = Product
    schema = ProductSchema

class UpdateDeleteProductResource(UpdateResource, DeleteResource):
    model = Product
    schema = ProductSchema

class OrderProductResource(Resource):
    def post(self):
        pass






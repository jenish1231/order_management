
from flask import request, jsonify, make_response

from .helper import *
from .models import *
from .schemas import *
from .decorators import *
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required)

class EmployeeListResource(ListResource, CreateResource):
    model = Employee
    schema = EmployeeSchema

    def post(self):
        response, status_code = super().post()
        if status_code == 200:
            access_token = create_access_token(identity=self.obj.email)

            return {
                'access_token': access_token
            }
            
        return response, status_code

    @employee_required
    def get(self):
        return super().get()

class EmployeeResource(DetailResource, DeleteResource):
    model = Employee
    schema = EmployeeSchema

   

class AddEmployeeToOfficeResource(GetObject, Resource):
    model = Office

    """
        validation : email
    """
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

class CustomerCreateResource(ListResource, CreateResource):
    model = Customer
    schema = CustomerSchema

    def post(self):
        response, status_code = super().post()
        if status_code == 200:
            access_token = create_access_token(identity=self.obj.email, user_claims={'customer':True})

            return {
                'access_token': access_token
            }
            
        return response, status_code

    @customer_required    
    def get(self):
        return super().get()

class LoginResource(Resource):
   

    def post(self):
        json_data = request.get_json()
        try:
            data = self.schema().load(json_data)
        except ValidationError as err:
            return err.messages, 400

        user = self.model.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.email)
            return {
                'access_token':access_token
            }
        return {"error": "Username or password incorrect!!"}, 400
    
class CustomerLoginResource(LoginResource):
    model = Customer
    schema = LoginSchema

class EmployeeLoginResource(LoginResource):
    model = Employee
    schema = LoginSchema


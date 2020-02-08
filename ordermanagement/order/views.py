
import string

from flask import jsonify, make_response, request

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required)

from .decorators import *
from .helper import *
from .models import *
from .schemas import *


def generate_token(user):
    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    return {'access_token': access_token, 'refresh_token': refresh_token }
    
class EmployeeListResource(ListResource, CreateResource):
    model = Employee
    schema = EmployeeSchema

    def post(self):
        response, status_code = super().post()
        if status_code == 200:
            return generate_token(self.obj)
        return response, status_code

    @employee_required
    def get(self):
        return super().get()

class EmployeeResource(DetailResource, DeleteResource):
    model = Employee
    schema = EmployeeSchema

   

class AddEmployeeToOfficeResource(Resource):
    model = Office

    def post(self, id):
        obj = get_object_or_404(self.model, id)
        json_data = request.get_json()

        try:
            employee_data = NewEmployeeSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 400
        employee_data['password'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        employee = Employee(**employee_data)
        employee.office_id = obj.office_code
        employee.save()
        
        return NewEmployeeSchema().dump(employee)

class OfficeCreateResource(CreateResource):
    model = Office
    schema = OfficeSchema

class ProductCreateResource(CreateResource):
    model = Product
    schema = ProductSchema

class UpdateDeleteProductResource(UpdateResource, DeleteResource):
    model = Product
    schema = ProductSchema



class CustomerCreateResource(ListResource, CreateResource):
    model = Customer
    schema = CustomerSchema

    def post(self):
        response, status_code = super().post()
        if status_code == 200:
            return generate_token(self.obj)
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
            return generate_token(user)
        return {"error": "Username or password incorrect!!"}, 400
    

class CustomerLoginResource(LoginResource):
    model = Customer
    schema = LoginSchema

class EmployeeLoginResource(LoginResource):
    model = Employee
    schema = LoginSchema

class OrderProductResource(Resource):
    schema = OrderSchema

    @customer_required
    def post(self, product_id):
        obj = get_object_or_404(Product, product_id)
        json_data = request.get_json()

        try:
            data = self.schema(extra=obj).load(json_data)
        except ValidationError as err:
            return err.messages, 400

        identity = get_jwt_identity()
        customer = Customer.query.filter_by(email=identity).first()

        order = Order(**data)
        order.ordered_date = datetime.datetime.now()
        order.customer_id = customer.customer_id
        
        obj.stock_quantity -= order.quantity
        order.save()

        
        return self.schema().dump(order)

class DeliverProductResource(Resource):
    schema = DeliverSchema
    
    @employee_required
    def post(self, order_id):
        identity = get_jwt_identity()
        employee = Employee.query.filter_by(email=identity).first()
        
        order = get_object_or_404(Order, order_id)
        
        deliver = Delivery(order_id=order.order_id, delivered_by_id=employee, delivered_date=datetime.datetime.now())
        order.shipped_date = datetime.datetime.now()
        deliver.save()

        return self.schema().dump(deliver)

class OrderListResource(ListResource):
    model = Order
    schema = OrderSchema

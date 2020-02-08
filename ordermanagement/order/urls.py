from flask_restful import Api
from flask import Blueprint
from .views import *

api_bp = Blueprint('api', __name__)

api = Api(api_bp)

url_patterns = [
    ('/products', ProductCreateResource),
    ('/product/<product_id>/order', OrderProduct),
    ('/product/<id>', UpdateDeleteProductResource),
    ('/offices', OfficeCreateResource),
    ('/office/<id>/add-employee', AddEmployeeToOfficeResource),
    ('/employees', EmployeeListResource),
    ('/employee/<id>', EmployeeResource),
    ('/customers', CustomerCreateResource),
    ('/customer/login', CustomerLoginResource),
    ('/employee/login', EmployeeLoginResource),
    
]

for url, view in url_patterns:
    api.add_resource(view, url)


from flask_restful import Api
from flask import Blueprint
from .views import *

api_bp = Blueprint('api', __name__)

api = Api(api_bp)

url_patterns = [
    ('/products', ProductCreateResource),
    ('/product/<int:product_id>/order', OrderProductResource),
    ('/product/<int:id>', UpdateDeleteProductResource),

    ('/offices', OfficeCreateResource),
    ('/office/<int:id>/add-employee', AddEmployeeToOfficeResource),

    ('/employees', EmployeeListResource),
    ('/employee/login', EmployeeLoginResource),
    ('/employee/<int:id>', EmployeeResource),
    
    ('/customers', CustomerCreateResource),
    ('/customer/login', CustomerLoginResource),
    
    ('/deliver/<int:order_id>', DeliverProductResource),
    ('/orders', OrderListResource)
    
]

for url, view in url_patterns:
    api.add_resource(view, url)


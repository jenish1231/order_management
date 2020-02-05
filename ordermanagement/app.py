from flask import Flask, Blueprint

from config import Config
from flask_migrate import Migrate
from flask_restful import Api

from order.models import db
from order.views import *

app = Flask(__name__)

#load configuration from Config file
app.config.from_object(Config())

db.init_app(app)
migrate = Migrate(app, db)

api_bp = Blueprint('api', __name__)

api = Api(api_bp)



# api.add_resource(ProductList, '/products')
# api.add_resource(Product, '/product/<id>')

# api.add_resource(Office, '/offices')
# api.add_resource(AddEmployeeToOffice, '/office/<id>/add-employee')

api.add_resource(ProductCreateResource, '/products')
api.add_resource(UpdateDeleteProductResource, '/product/<id>')

api.add_resource(OfficeCreateResource, '/offices')
api.add_resource(AddEmployeeToOfficeResource, '/office/<id>/add-employee')

api.add_resource(EmployeeListResource, '/employees')

app.register_blueprint(api_bp, url_prefix='/api')



@app.route('/')
def hello_world():
    return 'Hello, world!'



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

from flask import Flask

from config import Config
from flask_migrate import Migrate
from flask_restful import Api

from order.models import db
from order.views import *

app = Flask(__name__)
app.config.from_object(Config())

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)



@app.route('/')
def hello_world():
    return 'Hello, world!'


api.add_resource(ProductList, '/api/products')
api.add_resource(Product, '/api/product/<id>')

api.add_resource(Office, '/api/offices')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

from flask import Flask

from config import Config
from flask_migrate import Migrate

from order.models import db

app = Flask(__name__)
app.config.from_object(Config())

db.init_app(app)
migrate = Migrate(app, db)



@app.route('/')
def hello_world():
    return 'Hello, world!, again, another, and again, and again'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

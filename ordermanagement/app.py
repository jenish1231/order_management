from flask_migrate import Migrate
from server import app
from order.models import db
from order.urls import api_bp

migrate = Migrate(app, db)


app.register_blueprint(api_bp, url_prefix='/api')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


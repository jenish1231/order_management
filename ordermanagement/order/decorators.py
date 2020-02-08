
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import *
from server import app

def customer_required(func):
    """
        extends jwt_required and checks whether the user is Customer or Employee.
        if Employee return "Unauthorized"
    """

    with app.app_context():
        @jwt_required
        def inner(*args, **kwargs):
            identity = get_jwt_identity()
            user = Customer.query.filter_by(email=identity).first()
            if user:
                return func(*args, **kwargs)
            return {"error": "Unauthorized!"}, 401
        return inner

def employee_required(func):
    """
        extends jwt_required and checks whether the user is Customer or Employee.
        if Customer return "Unauthorized"
    """
    with app.app_context():
        @jwt_required
        def inner(*args, **kwargs):
            identity = get_jwt_identity()
            user = Employee.query.filter_by(email=identity).first()
            if user:
                return func(*args, **kwargs)
            return {"error": "Unauthorized!"}, 401
        return inner
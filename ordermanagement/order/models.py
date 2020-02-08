import jwt
from werkzeug.security import safe_str_cmp
import random

from flask_sqlalchemy import SQLAlchemy
from server import app, bcrypt
import datetime

db = SQLAlchemy(app)

products = db.Table('product_order', 
        db.Column('product_id', db.Integer, db.ForeignKey('product.product_id'), primary_key=True),
        db.Column('order_id', db.Integer, db.ForeignKey('order.order_id'), primary_key=True)
    )

class BaseModel(object):
    def save(self, *args, **kwargs):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, *args, **kwargs):
        kwargs['password'] = bcrypt.generate_password_hash(kwargs['password'])
        return super().__init__(*args, **kwargs)

    def __str__(self):
        return self.email

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Product(BaseModel, db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    name = db.Column(db.String(50), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    vendor = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return self.name

class Customer(User):
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(255))

    __mapper_args__ = {'inherit_condition': customer_id == User.id}

    def __str__(self):
        return self.name

    

class Office(BaseModel, db.Model):
    office_code = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)

    #employees

    def __str__(self):
        return str(self.office_code)

class Employee(User):
    employee_id = db.Column(db.Integer,  db.ForeignKey('user.id'), primary_key=True)
    job_title = db.Column(db.String(255), nullable=False)

    office_id = db.Column(db.Integer, db.ForeignKey('office.office_code'), nullable=True)
    office = db.relationship('Office', backref='employees')
    

    reports_to = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=True)
    employees = db.relationship('Employee', backref=db.backref('parent', remote_side='Employee.employee_id', ), primaryjoin='Employee.employee_id==Employee.reports_to')
    

    __mapper_args__ = {'inherit_condition': employee_id == User.id, 'polymorphic_identity':'Employee'}


    def __str__(self):
        return str(self.employee_id)


class Order(BaseModel, db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    ordered_date = db.Column(db.DateTime)
    shipped_date = db.Column(db.DateTime)
    comments = db.Column(db.Text)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    customer = db.relationship('Customer', backref='orders', lazy=True)

    # deliveries = db.relationship('Delivery', backref='order', lazy=True)
    products = db.relationship('Product', secondary=products, lazy='subquery', backref=db.backref('orders', lazy=True))

    def __str__(self):
        return str(self.order_id)


class Delivery(BaseModel, db.Model):
    delivery_id = db.Column(db.Integer, primary_key=True)
    delivered_date = db.Column(db.DateTime)

    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))

    delivered_by_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    delivered_by = db.relationship('Employee', backref='deliveries', lazy=True)

    def __str__(self):
        return str(self.delivery_id)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

products = db.Table('product_order', 
        db.Column('product_id', db.Integer, db.ForeignKey('product.product_id'), primary_key=True),
        db.Column('order_id', db.Integer, db.ForeignKey('order.order_id'), primary_key=True)
    )

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    name = db.Column(db.String(50), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    vendor = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return self.name

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, *args, **kwargs):
        self.password = bcrypt.generate_password_hash(password)
        super().__init__(*args, **kwargs)

        
    def __str__(self):
        return self.name

class Office(db.Model):
    office_code = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)

    #employees

    def __str__(self):
        return str(self.office_code)

class Employee(db.Model):
    employer_id = db.Column(db.Integer, primary_key=True)
    office_id = db.Column(db.Integer, db.ForeignKey('office.office_code'), nullable=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    job_title = db.Column(db.String(255), nullable=False)

    reports_to = db.Column(db.Integer, db.ForeignKey('employee.employer_id', on_delete="SET NULL"), nullable=True)

    deliveries = db.relationship('Delivery', backref='employee', lazy=True)
    employees = db.relationship('Employee', backref=db.backref('parent', remote_side='Employee.employer_id'))
    office = db.relationship('Office', backref='employees')

    def __str__(self):
        return str(self.employer_id)

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    quantity = db.Column(db.Integer)
    ordered_date = db.Column(db.DateTime)
    shipped_date = db.Column(db.DateTime)
    comments = db.Column(db.Text)

    deliveries = db.relationship('Delivery', backref='order', lazy=True)
    products = db.relationship('Product', secondary=products, lazy='subquery', backref=db.backref('orders', lazy=True))

    def __str__(self):
        return str(self.order_id)


class Delivery(db.Model):
    delivery_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
    delivered_by_id = db.Column(db.Integer, db.ForeignKey('employee.employer_id'))
    delivered_date = db.Column(db.DateTime)

    def __str__(self):
        return str(self.deliveryId)


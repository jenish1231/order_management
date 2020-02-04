from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

products = db.Table('product_order', 
        db.Column('productId', db.Integer, db.ForeignKey('product.productId'), primary_key=True),
        db.Column('orderId', db.Integer, db.ForeignKey('order.orderId'), primary_key=True)
    )

class Product(db.Model):
    productId = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    name = db.Column(db.String(255))
    stock_quantity = db.Column(db.Integer)
    vendor = db.Column(db.String(255))
    price = db.Column(db.Integer)

    def __str__(self):
        return self.name

class Customer(db.Model):
    customerId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __str__(self):
        return self.name

class Office(db.Model):
    office_code = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    state = db.Column(db.String(255))
    country = db.Column(db.String(255))

    def __str__(self):
        return str(self.office_code)

class Employee(db.Model):
    employerId = db.Column(db.Integer, primary_key=True)
    office_code = db.Column(db.Integer, db.ForeignKey('office.office_code'))
    reports_to = db.Column(db.Integer, db.ForeignKey('employee.employerId'), nullable=True)
    email = db.Column(db.String(255))
    job_title = db.Column(db.String(255))

    deliveries = db.relationship('Delivery', backref='employee', lazy=True)
    employees = db.relationship('Employee', backref='employee', lazy=True)

    def __str__(self):
        return str(self.employerId)

class Order(db.Model):
    orderId = db.Column(db.Integer, primary_key=True)
    customerId = db.Column(db.Integer, db.ForeignKey('customer.customerId'))
    quantity = db.Column(db.Integer)
    ordered_date = db.Column(db.DateTime)
    shipped_date = db.Column(db.DateTime)
    comments = db.Column(db.Text)

    # deliveries = db.relationship('Delivery', backref='order', lazy=True)
    products = db.relationship('Product', secondary=products, lazy='subquery', backref=db.backref('orders', lazy=True))

    def __str__(self):
        return str(self.orderId)


class Delivery(db.Model):
    deliveryId = db.Column(db.Integer, primary_key=True)
    orderId = db.Column(db.Integer, db.ForeignKey('order.orderId'))
    delivered_by = db.Column(db.Integer, db.ForeignKey('employee.employerId'))
    delivered_date = db.Column(db.DateTime)

    def __str__(self):
        return str(self.deliveryId)


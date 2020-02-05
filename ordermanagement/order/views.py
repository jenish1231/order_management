
from .models import *
from .schemas import *
from .mixins import *

class ProductList(CreateListResource):
    schema = ProductSchema
    model = Product

class Product(DetailUpdateDeleteResource):
    schema = ProductSchema
    model = Product

class Office(CreateListResource):
    schema = OfficeSchema
    model = Office

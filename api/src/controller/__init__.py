from flask import Blueprint
from flask_restx import Api
import sys, os, json, datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from routes.cart import ns as cart_namespace
from routes.consumer import ns as consumer_namespace
from routes.product import ns as product_namespace
from routes.producer import ns as producer_namespace
from routes.cart import ns as cart_namespace

NAME = 'api'
bp = Blueprint(
    NAME,
    __name__,
    url_prefix='/'
)

api = Api(
    bp,
    version='2022.11.25',
    title='Database Lecture Project',
    description='Online Shop API'
)

api.add_namespace(cart_namespace)
api.add_namespace(consumer_namespace)
api.add_namespace(product_namespace)
api.add_namespace(producer_namespace)

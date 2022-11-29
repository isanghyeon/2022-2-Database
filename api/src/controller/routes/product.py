from flask import g
from flask_restx import (
    Resource, fields, Namespace
)
from datetime import datetime
import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from controller.customizeField import StringToJSON
from controller.responseObj import responseObject
from models.shop.product import product as productDBModel

ns = Namespace('api/product', description='Product API EP')

RegistrationCartModel = ns.model('Product register model', {
    'idxProduct': fields.Integer(readonly=True, description=''),
    'ProductName': fields.String(required=True, description=''),
    'ProductCategory': fields.String(required=True, description=''),
    'ProductID': fields.String(required=True, description=''),
    'ProductOwnerID': fields.String(required=True, description=''),
    'ProductRemaining': fields.Integer(required=True, description=''),
    'ProductCost': fields.Integer(required=True, description=''),
    'ProductInformation': fields.String(required=True, description=''),
    'ProductImage': fields.String(required=True, description='')
})

GetCartModel = ns.model('Product get method response', {
    'idxProduct': fields.Integer(readonly=True, description=''),
    'ProductName': fields.String(required=True, description=''),
    'ProductCategory': fields.String(required=True, description=''),
    'ProductID': fields.String(required=True, description=''),
    'ProductOwnerID': fields.String(required=True, description=''),
    'ProductRemaining': fields.Integer(required=True, description=''),
    'ProductCost': fields.Integer(required=True, description=''),
    'ProductInformation': fields.String(required=True, description=''),
    'ProductImage': fields.String(required=True, description='')
})

Response = ns.model('Product Model - post/patch method response', {
    'status': fields.String(readonly=True, description=''),
    "message": fields.String(readonly=True, description='')
})


class daoProductObject(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""
        self.updateData = ""

    def ProductCount(self):
        self.counter = g.dbSession.query(productDBModel).count()
        return self.counter

    def productList(self):
        if self.ProductCount() == 0:
            ns.abort(404, f"Not Found")
        print(self.selectData)
        self.selectData = g.dbSession.query(productDBModel).all()

        if not self.selectData:
            ns.abort(404, f"Not Found")

        return self.selectData

    def keywordSearch(self, payload):
        if self.ProductCount() == 0:
            ns.abort(404, f"Not Found")

        self.selectData = g.dbSession.query(productDBModel).filter(productDBModel.ProductName.like(f'%{payload}%')).all()
        if not self.selectData:
            ns.abort(404, f"Not Found")

        return self.selectData

    def filter(self, payload):
        if self.ProductCount() == 0:
            ns.abort(404, f"Not Found")

        self.selectData = g.dbSession.query(productDBModel).filter(productDBModel.ProductCategory == payload).all()

        if not self.selectData:
            ns.abort(404, f"Not Found")

        return self.selectData

    @staticmethod
    def register(payload):
        if type(payload) is not dict:
            return responseObject().postMethodResponse(state=False)

        try:
            g.dbSession.add(productDBModel(
                ProductName=payload["ProductName"],
                ProductCategory=payload["ProductCategory"],
                ProductID=payload["ProductID"],
                ProductOwnerID=payload["ProductOwnerID"],
                ProductRemaining=payload["ProductRemaining"],
                ProductCost=payload["ProductCost"],
                ProductInformation=payload["ProductInformation"],
                ProductImage=payload["ProductImage"]
            ))
            g.dbSession.commit()

            return responseObject().postMethodResponse(state=True)
        except Exception as e:
            print("Product Registration ERROR :: ", e)
            g.dbSession.rollback()

        return responseObject().postMethodResponse(state=False)

    def delete(self, payload):
        print(payload, type(payload))

        if self.ProductCount() == 0:
            return responseObject().deleteMethodResponse(state=False)

        try:
            g.dbSession.query(productDBModel).filter(productDBModel.ProductID == payload).delete()
            g.dbSession.commit()
            return responseObject().deleteMethodResponse(state=True)
        except:
            g.dbSession.rollback()

        return responseObject().deleteMethodResponse(state=False)

    @staticmethod
    def modify(payload):
        if type(payload) is not dict:
            return responseObject().patchMethodResponse(state=False)

        try:
            g.dbSession.query(productDBModel).filter(productDBModel.ProductID == payload['ProductID']).update(
                {
                    "ProductName": payload['ProductName'],
                    "ProductCategory": payload['ProductCategory'],
                    "ProductID": payload['ProductID'],
                    "ProductOwnerID": payload['ProductOwnerID'],
                    "ProductRemaining": payload['ProductRemaining'],
                    "ProductCost": payload['ProductCost'],
                    "ProductInformation": payload['ProductInformation'],
                    "ProductImage": payload['ProductImage']
                }
            )
            g.dbSession.commit()
            return responseObject().patchMethodResponse(state=True)
        except:
            g.dbSession.rollback()

        return responseObject().patchMethodResponse(state=False)


handler = daoProductObject()


@ns.route('')
class epGetRequestHandler(Resource):
    """Request handler for Product Get"""

    @ns.doc('Get Product')
    @ns.marshal_list_with(GetCartModel)
    def get(self):
        """Fetch a given resource"""
        return handler.productList()


@ns.route('/filter/<string:filtering>')
@ns.response(404, 'Not Found')
@ns.param('filtering', 'keyword search in product category')
class epFilterRequestHandler(Resource):
    """Request handler for Product Filtering"""

    @ns.doc('Filter Product')
    @ns.marshal_list_with(GetCartModel)
    def get(self, filtering):
        """Fetch a given resource"""
        return handler.filter(filtering)


@ns.route('/search/<string:keyword>')
@ns.response(404, 'Not Found')
@ns.param('keyword', 'keyword search in product name')
class epSearchRequestHandler(Resource):
    """Request handler for Product Search"""

    @ns.doc('Search Product')
    @ns.marshal_list_with(GetCartModel)
    def get(self, keyword):
        """Fetch a given resource"""
        return handler.keywordSearch(keyword)


@ns.route('/register')
class epRegisterRequestHandler(Resource):
    """Request handler for Product Register"""

    @ns.doc('Registration Product')
    @ns.expect(RegistrationCartModel)
    @ns.marshal_with(Response)
    def post(self):
        """Fetch a given resource"""
        return handler.register(ns.payload)


@ns.route('/delete/<string:productID>')
@ns.response(404, 'Not Found')
@ns.param('productID', 'productID search in product information')
class epModifyRequestHandler(Resource):
    """Request handler for modify"""

    @ns.doc('Delete Product')
    @ns.marshal_with(Response)
    def delete(self, productID):
        """Fetch a given resource"""
        return handler.delete(productID)


@ns.route('/modify')
class epModifyRequestHandler(Resource):
    """Request handler for modify"""

    @ns.doc('Modify Product')
    @ns.expect(GetCartModel)
    @ns.marshal_with(Response)
    def patch(self):
        """Fetch a given resource"""
        return handler.modify(ns.payload)

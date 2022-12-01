from flask import g
from flask_restx import (
    Resource, fields, Namespace
)
from datetime import datetime
import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controller.responseObj import responseObject
from models.shop.cart import cart as cartDBModel

ns = Namespace('api/cart', description='Cart API EP')

cartModel = ns.model('Cart register model', {
    'idxCart': fields.Integer(readonly=True, description=''),
    'CartProductName': fields.String(required=True, description=''),
    'CartProductID': fields.String(required=True, description=''),
    'CartProductCost': fields.Integer(required=True, description=''),
    'CartProductImage': fields.String(required=True, description=''),
    'ConsumerIdentifyNumber': fields.String(required=True, description=''),
    'CartBuyChecked': fields.Boolean(required=True, description=''),
    "UpdateTimestamp": fields.DateTime(required=True, description='')
})

cartRemoveModel = ns.model('Cart Model - remove', {
    'status': fields.String(readonly=True, description=''),
    "message": fields.String(readonly=True, description='')
})

cartBoughtModel = ns.model('Cart Model - buy', {
    'status': fields.String(readonly=True, description=''),
    "message": fields.String(readonly=True, description='')
})

cartListModel = ns.model('Cart Model - list', {
    'status': fields.String(readonly=True, description=''),
    "message": fields.String(readonly=True, description='')
})

Response = ns.model('Cart Model - post/patch method response', {
    'status': fields.String(readonly=True, description=''),
    "message": fields.String(readonly=True, description='')
})


class daoCartObject(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""
        self.updateData = ""

    def CartCount(self):
        self.counter = g.dbSession.query(cartDBModel).count()
        return self.counter

    @staticmethod
    def CartRegister(payload):
        if type(payload) is not dict:
            return responseObject().postMethodResponse(state=False)

        try:
            g.dbSession.add(cartDBModel(
                CartProductName=payload["CartProductName"],
                CartProductID=payload["CartProductID"],
                CartProductCost=payload["CartProductCost"],
                CartProductImage=payload["CartProductImage"],
                ProducerIdentifyNumber='635265ac-6cb9-11ed-bef8-acde48001122',
                ConsumerIdentifyNumber=payload["ConsumerIdentifyNumber"],
                CartBuyChecked=payload["CartBuyChecked"],
                UpdateTimestamp=payload["UpdateTimestamp"]
            ))
            g.dbSession.commit()

            return responseObject().postMethodResponse(state=True)
        except Exception as e:
            print("Cart Sign Up ERROR :: ", e)
            g.dbSession.rollback()

        return responseObject().postMethodResponse(state=False)

    def CartRemove(self, payload):
        if self.ProductCount() == 0:
            return responseObject().deleteMethodResponse(state=False)

        try:
            g.dbSession.query(cartDBModel).filter(cartDBModel.CartProductID == payload["CartProductID"],
                                                  cartDBModel.ConsumerIdentifyNumber == payload["ConsumerIdentifyNumber"]).delete()
            g.dbSession.commit()
            return responseObject().deleteMethodResponse(state=True)
        except:
            g.dbSession.rollback()

        return responseObject().deleteMethodResponse(state=False)

    def CartBuy(self, payload):
        if self.CartCount() == 0:
            return responseObject().patchMethodResponse(state=False)

        try:
            g.dbSession.query(cartDBModel).filter(cartDBModel.ConsumerIdentifyNumber == payload["ConsumerIdentifyNumber"]).update(
                {'CartBuyChecked': 1}
            )
            g.dbSession.commit()
            return responseObject().patchMethodResponse(state=True)
        except:
            g.dbSession.rollback()
        return responseObject().patchMethodResponse(state=False)

    def CartProductsList(self, payload):
        if self.CartCount() == 0:
            ns.abort(404, f"Not Found")

        self.selectData = g.dbSession.query(cartDBModel).filter(cartDBModel.ConsumerIdentifyNumber == payload["ConsumerIdentifyNumber"], cartDBModel.CartBuyChecked == 0).all()

        if not self.selectData:
            ns.abort(404, f"Not Found")

        return self.selectData

    def CartBuyProductsList(self, payload):
        if self.CartCount() == 0:
            ns.abort(404, f"Not Found")

        self.selectData = g.dbSession.query(cartDBModel).filter(cartDBModel.ConsumerIdentifyNumber == payload["ConsumerIdentifyNumber"], cartDBModel.CartBuyChecked == 1).all()

        if not self.selectData:
            ns.abort(404, f"Not Found")

        return self.selectData


handler = daoCartObject()


@ns.route('/register')
class epRegisterRequestHandler(Resource):
    """Request handler for Cart Registered"""

    @ns.doc('Register Cart')
    @ns.expect(cartModel)
    @ns.marshal_with(Response)
    def post(self):
        """Fetch a given resource"""
        return handler.CartRegister(ns.payload)


@ns.route('/remove/<string:ConsumerIdentifyNumber>/<string:CartProductID>')
@ns.response(404, 'Not Found')
@ns.param('ConsumerIdentifyNumber', 'Consumer Identity Number')
@ns.param('CartProductID', 'Cart Identity Number')
class epRemoveRequestHandler(Resource):
    """Request handler for Cart Removed"""

    @ns.doc('Remove Cart')
    @ns.marshal_with(Response)
    def delete(self, ConsumerIdentifyNumber, CartProductID):
        """Fetch a given resource"""
        return handler.CartRemove({"ConsumerIdentifyNumber": ConsumerIdentifyNumber, "CartProductID": CartProductID})


@ns.route('/products/<string:ConsumerIdentifyNumber>')
@ns.response(404, 'Not Found')
@ns.param('ConsumerIdentifyNumber', 'Consumer Identity Number')
class epProductsRequestHandler(Resource):
    """Request handler for Cart List"""

    @ns.doc('Get Cart')
    @ns.marshal_list_with(cartModel)
    def get(self, ConsumerIdentifyNumber):
        """Fetch a given resource"""
        return handler.CartProductsList({"ConsumerIdentifyNumber": ConsumerIdentifyNumber})


@ns.route('/products/buy/<string:ConsumerIdentifyNumber>')
@ns.response(404, 'Not Found')
@ns.param('ConsumerIdentifyNumber', 'Consumer Identity Number')
class epProductsBuyRequestHandler(Resource):
    """Request handler for buy Cart List"""

    @ns.doc('Get Buy Cart')
    @ns.marshal_list_with(cartModel)
    def get(self, ConsumerIdentifyNumber):
        """Fetch a given resource"""
        return handler.CartBuyProductsList({"ConsumerIdentifyNumber": ConsumerIdentifyNumber})


@ns.route('/buy/<string:ConsumerIdentifyNumber>')
@ns.response(404, 'Not Found')
@ns.param('ConsumerIdentifyNumber', 'Consumer Identity Number')
class epBuyRequestHandler(Resource):
    """Request handler for Cart Bought"""

    @ns.doc('Buy Product')
    @ns.marshal_with(Response)
    def patch(self, ConsumerIdentifyNumber):
        """Fetch a given resource"""
        return handler.CartBuy({"ConsumerIdentifyNumber": ConsumerIdentifyNumber})

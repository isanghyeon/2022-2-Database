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
    'CartID': fields.String(required=True, description=''),
    'CartProductName': fields.String(required=True, description=''),
    'CartProductCategory': fields.String(required=True, description=''),
    'CartProductID': fields.String(required=True, description=''),
    'CartProductRemaining': fields.Integer(required=True, description=''),
    'CartProductCost': fields.Integer(required=True, description=''),
    'CartProductInformation': fields.String(required=True, description=''),
    'ProducerIdentifyNumber': fields.String(required=True, description=''),
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
                CartProductCategory=payload["CartProductCategory"],
                CartProductID=payload["CartProductID"],
                CartProductRemaining=payload["CartProductRemaining"],
                CartProductCost=payload["CartProductCost"],
                CartProductInformation=payload["CartProductInformation"],
                ProducerIdentifyNumber=payload["ProducerIdentifyNumber"],
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

    def CartRemove(self):
        pass

    def CartBuy(self):
        pass

    def CartProductsList(self, payload):
        if self.CartCount() == 0 or type(payload) is not dict or not len(payload["CartEmail"]) or not len(payload["CartPWD"]):
            return responseObject().postMethodResponse(state=False)

        self.selectData = g.dbSession.query(cartDBModel).filter(cartDBModel.CartEmail == payload["CartEmail"],
                                                                cartDBModel.CartPWD == payload["CartPWD"]).first()

        if not self.selectData:
            return responseObject().postMethodResponse(state=False)

        return responseObject().postMethodResponse(state=True)

    # def modify(self, payload):
    #     if type(payload) is not dict or not len(payload["data"]):
    #         return responseObject().return_post_http_status_message()
    #
    #     try:
    #         g.dbSession.query(cartDBModel).filter(jobModel.id == int(self.updateData[ListofData]["id"])).update(
    #             {'done': int(self.updateData[ListofData]["done"])}
    #         )
    #         g.dbSession.commit()
    #         return Return_object().return_patch_http_status_message(Type=True)
    #     except:
    #         g.dbSession.rollback()
    #
    #     return Return_object().return_patch_http_status_message(Type=False)


handler = daoCartObject()


@ns.route('/register')
class epRegisterRequestHandler(Resource):
    """Request handler for Cart Registered"""

    @ns.doc('Get Cart')
    @ns.expect()
    @ns.marshal_with()
    def post(self):
        """Fetch a given resource"""
        return handler.CartRegister(ns.payload)


@ns.route('/remove')
class epRemoveRequestHandler(Resource):
    """Request handler for Cart Removed"""

    @ns.doc('Get Cart')
    @ns.expect()
    @ns.marshal_with()
    def delete(self):
        """Fetch a given resource"""
        return handler.CartRemove(ns.payload)


@ns.route('/products/<string:id>')
@ns.response(404, 'Not Found')
@ns.param('id', 'Cart Identity Number')
class epProductsRequestHandler(Resource):
    """Request handler for Cart List"""

    @ns.doc('Create Cart')
    @ns.expect()
    @ns.marshal_with()
    def get(self):
        """Fetch a given resource"""
        return handler.CartProductsList(ns.payload)


@ns.route('/buy')
class epBuyRequestHandler(Resource):
    """Request handler for Cart Bought"""

    @ns.doc('Create Cart')
    @ns.expect()
    @ns.marshal_with()
    def post(self):
        """Fetch a given resource"""
        return handler.CartBuy(ns.payload)

# @ns.route('/modify')
# class epModifyRequestHandler(Resource):
#     """Request handler for modify"""
#
#     @ns.doc('Modify Cart')
#     @ns.expect()
#     @ns.marshal_with()
#     def patch(self):
#         """Fetch a given resource"""
#         return handler.update(ns.payload)

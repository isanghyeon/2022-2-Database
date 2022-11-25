from flask import g
from flask_restx import (
    Resource, fields, Namespace
)
from datetime import datetime
import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controller.customizeField import StringToJSON
from controller.responseObj import responseObject
from models.shop.product import product as productDBModel

ns = Namespace('api/product', description='Product API EP')

cartModel = ns.model('Product register model', {
    'idxProduct': fields.Integer(readonly=True, description=''),
    'ProductName': fields.String(required=True, description=''),
    'ProductCategory': fields.String(required=True, description=''),
    'ProductID': fields.String(required=True, description=''),
    'ProductOwnerID': fields.String(required=True, description=''),
    'ProductRemaining': fields.Integer(required=True, description=''),
    'ProductCost': fields.Integer(required=True, description=''),
    'ProductInformation': fields.String(required=True, description=''),
    'ProductImage': StringToJSON(required=True, description='')
})

signinModel = ns.model('Product login model', {
    'ProductEmail': fields.String(required=True, description=''),
    'ProductPWD': fields.String(required=True, description='')
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

    def signIn(self, payload):
        if self.ProductCount() == 0 or type(payload) is not dict or not len(payload["ProductEmail"]) or not len(payload["ProductPWD"]):
            return responseObject().postMethodResponse(state=False)

        self.selectData = g.dbSession.query(productDBModel).filter(productDBModel.ProductEmail == payload["ProductEmail"],
                                                                    productDBModel.ProductPWD == payload["ProductPWD"]).first()

        if not self.selectData:
            return responseObject().postMethodResponse(state=False)

        return responseObject().postMethodResponse(state=True)

    @staticmethod
    def signUp(payload):
        if type(payload) is not dict:
            return responseObject().postMethodResponse(state=False)

        try:
            g.dbSession.add(productDBModel(
                ProductEmail=payload["ProductEmail"],
                ProductPWD=payload["ProductPWD"],
                ProductName=payload["ProductName"],
                Address=payload["Address"],
                PhoneNumber=payload["PhoneNumber"],
                ClassificationNumber=payload["ClassificationNumber"],
                IdentifyNumber=payload["IdentifyNumber"],
                LastLogin=payload["LastLogin"],
                CreateTime=payload["CreateTime"]
            ))
            g.dbSession.commit()

            return responseObject().postMethodResponse(state=True)
        except Exception as e:
            print("Product Sign Up ERROR :: ", e)
            g.dbSession.rollback()

        return responseObject().postMethodResponse(state=False)

    # def modify(self, payload):
    #     if type(payload) is not dict or not len(payload["data"]):
    #         return responseObject().return_post_http_status_message()
    #
    #     try:
    #         g.dbSession.query(productDBModel).filter(jobModel.id == int(self.updateData[ListofData]["id"])).update(
    #             {'done': int(self.updateData[ListofData]["done"])}
    #         )
    #         g.dbSession.commit()
    #         return Return_object().return_patch_http_status_message(Type=True)
    #     except:
    #         g.dbSession.rollback()
    #
    #     return Return_object().return_patch_http_status_message(Type=False)


handler = daoProductObject()


@ns.route('/signin')
class epSigninRequestHandler(Resource):
    """Request handler for Product Sign In"""

    @ns.doc('Get Product')
    @ns.expect(signinModel)
    @ns.marshal_with(Response)
    def post(self):
        """Fetch a given resource"""
        return handler.signIn(ns.payload)


@ns.route('/signup')
class epSignupRequestHandler(Resource):
    """Request handler for Product Sign Up"""

    @ns.doc('Create Product')
    @ns.expect(signupModel)
    @ns.marshal_with(Response)
    def post(self):
        """Fetch a given resource"""
        return handler.signUp(ns.payload)

# @ns.route('/modify')
# class epModifyRequestHandler(Resource):
#     """Request handler for modify"""
#
#     @ns.doc('Modify Product')
#     @ns.expect()
#     @ns.marshal_with()
#     def patch(self):
#         """Fetch a given resource"""
#         return handler.update(ns.payload)

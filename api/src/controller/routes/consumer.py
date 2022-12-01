from flask import g
from flask_restx import (
    Resource, fields, Namespace
)
from datetime import datetime
import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controller.responseObj import responseObject
from controller.customizeField import StringToJSON
from models.shop.consumer import consumer as consumerDBModel

ns = Namespace('api/consumer', description='Consumer API EP')

signupModel = ns.model('Consumer register model', {
    'idxConsumer': fields.Integer(readonly=True, description=''),
    'ConsumerEmail': fields.String(required=True, description=''),
    'ConsumerPWD': fields.String(required=True, description=''),
    'ConsumerName': fields.String(required=True, description=''),
    'Address': fields.String(required=True, description=''),
    'PhoneNumber': fields.String(required=True, description=''),
    'ClassificationNumber': fields.Integer(required=True, description=''),
    'IdentifyNumber': fields.String(required=True, description=''),
    'LastLogin': fields.DateTime(required=True, description=''),
    'CreateTime': fields.DateTime(required=True, description='')
})

consumerModel = ns.model('Consumer data  model', {
    'idxConsumer': fields.Integer(readonly=True, description=''),
    'ConsumerEmail': fields.String(required=True, description=''),
    'ConsumerName': fields.String(required=True, description=''),
    'Address': fields.String(required=True, description=''),
    'PhoneNumber': fields.String(required=True, description=''),
    'IdentifyNumber': fields.String(required=True, description='')
})

consumerBuyModel = ns.model('Consumer buy data  model', {
    'idxConsumer': fields.Integer(readonly=True, description=''),
    'ConsumerEmail': fields.String(required=True, description='')
})

signinModel = ns.model('Consumer login model', {
    'ConsumerEmail': fields.String(required=True, description=''),
    'ConsumerPWD': fields.String(required=True, description='')
})
#
# notUsed = ns.model('Consumer modify model', {
#
# })

Response = ns.model('Consumer Model - post/patch method response', {
    'status': fields.String(readonly=True, description=''),
    "message": fields.String(readonly=True, description='')
})


class daoConsumerObject(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""
        self.updateData = ""

    def consumerCount(self):
        self.counter = g.dbSession.query(consumerDBModel).count()
        return self.counter

    def getConsumerList(self, payload):
        if self.consumerCount() == 0:
            ns.abort(404, f"Not Found")
        self.selectData = g.dbSession.query(consumerDBModel.idxConsumer, consumerDBModel.ConsumerEmail, consumerDBModel.ConsumerName, consumerDBModel.Address,
                                            consumerDBModel.PhoneNumber, consumerDBModel.IdentifyNumber).filter(consumerDBModel.ConsumerEmail == payload).first()

        if not self.selectData:
            ns.abort(404, f"Not Found")

        return self.selectData

    def signIn(self, payload):
        if self.consumerCount() == 0 or type(payload) is not dict or not len(payload["ConsumerEmail"]) or not len(payload["ConsumerPWD"]):
            return responseObject().postMethodResponse(state=False)

        self.selectData = g.dbSession.query(consumerDBModel).filter(consumerDBModel.ConsumerEmail == payload["ConsumerEmail"],
                                                                    consumerDBModel.ConsumerPWD == payload["ConsumerPWD"]).first()

        if not self.selectData:
            return responseObject().postMethodResponse(state=False)

        return responseObject().postMethodResponse(state=True)

    @staticmethod
    def signUp(payload):
        if type(payload) is not dict:
            return responseObject().postMethodResponse(state=False)

        try:
            g.dbSession.add(consumerDBModel(
                ConsumerEmail=payload["ConsumerEmail"],
                ConsumerPWD=payload["ConsumerPWD"],
                ConsumerName=payload["ConsumerName"],
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
            print("Consumer Sign Up ERROR :: ", e)
            g.dbSession.rollback()

        return responseObject().postMethodResponse(state=False)

    # def modify(self, payload):
    #     if type(payload) is not dict:
    #         return responseObject().patchMethodResponse(state=False)
    #
    #     try:
    #         self.selectData = g.dbSession.query(consumerDBModel.BuyProductID).filter(consumerDBModel.ConsumerEmail == payload["ConsumerEmail"]).first()
    #         print("======= =====")
    #         print(self.selectData, type(self.selectData))
    #         print("======= =====")
    #         print(payload["BuyProductID"])
    #         g.dbSession.query(consumerDBModel).filter(consumerDBModel.ConsumerEmail == payload["ConsumerEmail"]).update(
    #             {'BuyProductID': json.dumps(payload["BuyProductID"])}
    #         )
    #         g.dbSession.commit()
    #         return responseObject().patchMethodResponse(state=True)
    #     except:
    #         g.dbSession.rollback()
    #
    #     return responseObject().patchMethodResponse(state=False)


handler = daoConsumerObject()


@ns.route('/consumer/<string:ConsumerEmail>')
@ns.response(404, 'Not Found')
@ns.param('ConsumerEmail', 'Consumer Email')
class epOneGetRequestHandler(Resource):
    """Request handler for Consumer Data"""

    @ns.doc('Get Consumer Data')
    @ns.marshal_with(consumerModel)
    def get(self, ConsumerEmail):
        """Fetch a given resource"""
        return handler.getConsumerList(ConsumerEmail)


@ns.route('/signin')
class epSigninRequestHandler(Resource):
    """Request handler for Consumer Sign In"""

    @ns.doc('Get Consumer')
    @ns.expect(signinModel)
    @ns.marshal_with(Response)
    def post(self):
        """Fetch a given resource"""
        return handler.signIn(ns.payload)


@ns.route('/signup')
class epSignupRequestHandler(Resource):
    """Request handler for Consumer Sign Up"""

    @ns.doc('Create Consumer')
    @ns.expect(signupModel)
    @ns.marshal_with(Response)
    def post(self):
        """Fetch a given resource"""
        return handler.signUp(ns.payload)


# @ns.route('/modify')
# class epModifyRequestHandler(Resource):
#     """Request handler for modify"""
#
#     @ns.doc('Modify Consumer')
#     @ns.expect(consumerBuyModel)
#     @ns.marshal_with(Response)
#     def patch(self):
#         """Fetch a given resource"""
#         return handler.modify(ns.payload)

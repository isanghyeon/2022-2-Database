from flask import g
from flask_restx import (
    Resource, fields, Namespace
)
from datetime import datetime
import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controller.responseObj import responseObject
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
    #     if type(payload) is not dict or not len(payload["data"]):
    #         return responseObject().return_post_http_status_message()
    #
    #     try:
    #         g.dbSession.query(consumerDBModel).filter(jobModel.id == int(self.updateData[ListofData]["id"])).update(
    #             {'done': int(self.updateData[ListofData]["done"])}
    #         )
    #         g.dbSession.commit()
    #         return Return_object().return_patch_http_status_message(Type=True)
    #     except:
    #         g.dbSession.rollback()
    #
    #     return Return_object().return_patch_http_status_message(Type=False)


handler = daoConsumerObject()


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
#     @ns.expect()
#     @ns.marshal_with()
#     def patch(self):
#         """Fetch a given resource"""
#         return handler.update(ns.payload)

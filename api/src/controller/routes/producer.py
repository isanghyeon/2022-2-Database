from flask import g
from flask_restx import (
    Resource, fields, Namespace
)
from datetime import datetime
import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controller.responseObj import responseObject
from models.shop.producer import producer as producerDBModel

ns = Namespace('api/producer', description='Producer API EP')

signupModel = ns.model('Producer register model', {
    'idxProducer': fields.Integer(readonly=True, description=''),
    'ProducerEmail': fields.String(required=True, description=''),
    'ProducerPWD': fields.String(required=True, description=''),
    'ProducerName': fields.String(required=True, description=''),
    'Address': fields.String(required=True, description=''),
    'PhoneNumber': fields.String(required=True, description=''),
    'ClassificationNumber': fields.Integer(required=True, description=''),
    'IdentifyNumber': fields.String(required=True, description=''),
    'LastLogin': fields.DateTime(required=True, description=''),
    'CreateTime': fields.DateTime(required=True, description='')
})

signinModel = ns.model('Producer login model', {
    'ProducerEmail': fields.String(required=True, description=''),
    'ProducerPWD': fields.String(required=True, description='')
})
#
# notUsed = ns.model('Producer modify model', {
#
# })

Response = ns.model('Producer Model - post/patch method response', {
    'status': fields.String(readonly=True, description=''),
    "message": fields.String(readonly=True, description='')
})


class daoProducerObject(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""
        self.updateData = ""

    def ProducerCount(self):
        self.counter = g.dbSession.query(producerDBModel).count()
        return self.counter

    def signIn(self, payload):
        if self.ProducerCount() == 0 or type(payload) is not dict or not len(payload["ProducerEmail"]) or not len(payload["ProducerPWD"]):
            return responseObject().postMethodResponse(state=False)

        self.selectData = g.dbSession.query(producerDBModel).filter(producerDBModel.ProducerEmail == payload["ProducerEmail"],
                                                                    producerDBModel.ProducerPWD == payload["ProducerPWD"]).first()

        if not self.selectData:
            return responseObject().postMethodResponse(state=False)

        return responseObject().postMethodResponse(state=True)

    @staticmethod
    def signUp(payload):
        if type(payload) is not dict:
            return responseObject().postMethodResponse(state=False)

        try:
            g.dbSession.add(producerDBModel(
                ProducerEmail=payload["ProducerEmail"],
                ProducerPWD=payload["ProducerPWD"],
                ProducerName=payload["ProducerName"],
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
            print("Producer Sign Up ERROR :: ", e)
            g.dbSession.rollback()

        return responseObject().postMethodResponse(state=False)

    # def modify(self, payload):
    #     if type(payload) is not dict or not len(payload["data"]):
    #         return responseObject().return_post_http_status_message()
    #
    #     try:
    #         g.dbSession.query(producerDBModel).filter(jobModel.id == int(self.updateData[ListofData]["id"])).update(
    #             {'done': int(self.updateData[ListofData]["done"])}
    #         )
    #         g.dbSession.commit()
    #         return Return_object().return_patch_http_status_message(Type=True)
    #     except:
    #         g.dbSession.rollback()
    #
    #     return Return_object().return_patch_http_status_message(Type=False)


handler = daoProducerObject()


@ns.route('/signin')
class epSigninRequestHandler(Resource):
    """Request handler for Producer Sign In"""

    @ns.doc('Get Producer')
    @ns.expect(signinModel)
    @ns.marshal_with(Response)
    def post(self):
        """Fetch a given resource"""
        return handler.signIn(ns.payload)


@ns.route('/signup')
class epSignupRequestHandler(Resource):
    """Request handler for Producer Sign Up"""

    @ns.doc('Create Producer')
    @ns.expect(signupModel)
    @ns.marshal_with(Response)
    def post(self):
        """Fetch a given resource"""
        return handler.signUp(ns.payload)

# @ns.route('/modify')
# class epModifyRequestHandler(Resource):
#     """Request handler for modify"""
#
#     @ns.doc('Modify Producer')
#     @ns.expect()
#     @ns.marshal_with()
#     def patch(self):
#         """Fetch a given resource"""
#         return handler.update(ns.payload)

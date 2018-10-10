import jwt
import datetime
import json
from flask import jsonify
from server.Structures.Response import Responses
from server.Communication.DatabaseCommunication.userTransactions import UserTransactions
from server.Communication.facebookCommunication import FacebookCommunication
import logging
from server.setup import app
import logging
with app.app_context():
    secret_key = app.config.get('SECRET_KEY')
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


class UserServices:

    @staticmethod
    def __updateUser(data):
        UserTransactions.updateUserData(data)

    @staticmethod
    def __registerNonExistingUser(data):
        exp_date = UserServices.__getDateTime()
        UserTransactions.newUser(data["facebookId"], data["firstName"],
                                 data["lastName"], data["photoUrl"], data["email"])
        token = UserServices.__generateToken(data["facebookId"], exp_date)
        return token

    @staticmethod
    def __checkUserExistance(facebook_id):
        user = UserTransactions.findUserById(facebook_id)
        return not (user is None)

    @staticmethod
    def __getDateTime():
        return datetime.datetime.utcnow() + datetime.timedelta(seconds=900)

    @staticmethod
    def __generateToken(facebook_id, exp_date):
        payload = {"user": facebook_id,
                   "exp": exp_date}
        token = jwt.encode(payload, secret_key)
        UserTransactions.updateUserToken(facebook_id, token, exp_date)
        return token.decode('UTF-8')

    @staticmethod
    def checkLogin(request_data):
        facebook_id = request_data["facebookId"]
        if FacebookCommunication.ValidateUser(facebook_id, request_data["token"]):
            if UserServices.__checkUserExistance(facebook_id):
                response = {'token': UserServices.__generateToken(facebook_id, UserServices.__getDateTime())}
                return Responses.success('Token generado correctamente', response)
            else:
                return Responses.unauthorized('Usuario no registrado')
        else:
            return Responses.badRequest('FacebookId Invalido')

    @staticmethod
    def registerUser(request_data):
        if FacebookCommunication.ValidateUser(request_data["facebookId"], request_data["token"]):
            if not UserServices.__checkUserExistance(facebook_id):
                response = {'token': UserServices.__registerNonExistingUser(request_data)}
                return Responses.success('Usuario registrado correctamente', response)
            else:
                return Responses.badRequest('Usuario ya registrado')
        else:
            return Responses.badRequest('FacebookId Invalido')

    @staticmethod
    def updateUser(request_data):
        if FacebookCommunication.ValidateUser(request_data["facebookId"], request_data["token"]):
            if UserServices.__checkUserExistance(facebook_id):
                UserServices.__updateUser(request_data)
                return Responses.success('Usuario actualizado correctamente', "")
            else:
                return Responses.badRequest('Usuario no registrado')
        else:
            return Responses.badRequest('FacebookId Invalido')

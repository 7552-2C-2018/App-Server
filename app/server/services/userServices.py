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
    def __registerNonExistingUser(facebook_id, exp_date):
        UserTransactions.newUser(facebook_id)
        token = UserServices.__generateToken(facebook_id, exp_date)
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
        facebook_token = request_data["token"]
        facebook_response = FacebookCommunication.ValidateUser(facebook_token)
        facebook_payload = json.loads(facebook_response.text)
        if facebook_response.status_code == 200 and facebook_payload['id'] == facebook_id:
            if UserServices.__checkUserExistance(facebook_id):
                response = {'token': UserServices.__generateToken(facebook_id, UserServices.__getDateTime())}
                return Responses.success('Token generado correctamente', response)
            else:
                return Responses.unauthorized('Usuario no registrado')
        else:
            return Responses.badRequest('FacebookId Invalido')


    @staticmethod
    def registerUser(request_data):
        facebook_id = request_data["facebookId"]
        facebook_token = request_data["token"]
        facebook_response = FacebookCommunication.ValidateUser(facebook_token)
        facebook_payload = json.loads(facebook_response.text)
        if facebook_response.status_code == 200 and facebook_payload['id'] == facebook_id:
            if not UserServices.__checkUserExistance(facebook_id):
                response = {'token': UserServices.__registerNonExistingUser(facebook_id, UserServices.__getDateTime())}
                return Responses.success('Usuario registrado correctamente', response)
            else:
                return Responses.badRequest('Usuario ya registrado')
        else:
            return Responses.badRequest('FacebookId Invalido')

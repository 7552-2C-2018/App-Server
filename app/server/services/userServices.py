import jwt
import datetime
from flask import jsonify
from server.Structures.Response import Responses
from server.Communication.DatabaseCommunication.userTransactions import UserTransactions
from server.Communication.facebookCommunication import FacebookCommunication

class UserServices:

    @staticmethod
    def __registerNonExistingUser(facebook_id, exp_date):
        token = __generateToken(facebook_id, exp_date)
        UserTransactions.newUser(facebook_id, token, exp_date)
        return token

    @staticmethod
    def __checkUserExistance(facebook_id):
        return UserTransactions.findUserById(facebook_id) is None

    @staticmethod
    def __getDateTime():
        return datetime.datetime.utcnow() + datetime.timedelta(seconds=900)

    @staticmethod
    def __generateToken(facebook_id, exp_date):
        payload = {"user": facebook_id,
                   "exp": exp_date}
        token = jwt.encode(payload, app.config.get('SECRET_KEY'))
        UserTransactions.updateUserToken(facebook_id, token, expdate)
        return token.decode('UTF-8')

    @staticmethod
    def checkLogin(request_data):
        facebook_id = request_data["facebookId"]
        facebook_token = request_data["token"]
        facebook_response = FacebookCommunication.ValidateUser(facebook_token)
        response = []
        if facebook_response.status_code == 200 and facebook_response[id] == facebook_id:
            if checkUserExistance:
                response['token'] = __generateToken(facebook_id, __getDateTime())
            else:
                return Responses.unauthorized('Usuario no registrado')
        else:
            return Responses.badRequest('FacebookId Invalido')
        return Responses.success(response)


    @staticmethod
    def registerUser(request):
        request_data = request.body
        facebook_id = request_data["facebookId"]
        facebook_response = FacebookCommunication.ValidateUser(facebook_token)
        if facebook_response.status_code == 200 and facebook_response[id] == facebook_id:
            if not __checkUserExistance:
                response['token'] = __registerNonExistingUser(facebook_id, __getDateTime())
            else:
                Responses.badRequest('Usuario ya registrado')
        else:
            Responses.badRequest('FacebookId Invalido')
        return Responses.success(response)
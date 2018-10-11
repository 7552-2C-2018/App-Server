from functools import wraps
from flask import request
import datetime
import time
from server.Structures.Response import Responses
from server.Communication.DatabaseCommunication.userTransactions import UserTransactions
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

def validateAuth(function):

    @wraps(function)
    def validateAuthorization(*args, **kwargs):

        user = UserTransactions.findUserById(request.headers.get('facebookId'))
        if user is None:
            return_data = Responses.unauthorized('FacebookId not found') 
            return return_data["data"], return_data["status"], {'message': return_data["message"]}
        token = request.headers.get('token')

        if token != user['token']:
            return_data = Responses.unauthorized('Invalid token')
            return return_data["data"], return_data["status"], {'message': return_data["message"]}

        current_date_seconds = time.mktime(datetime.datetime.utcnow().timetuple())
        exp_date_seconds = time.mktime(user['exp_date'].timetuple())
        if current_date_seconds > exp_date_seconds:
            return_data = Responses.unauthorized('Expirated token')
            return return_data["data"], return_data["status"], {'message': return_data["message"]}

        return function(*args, **kwargs)

    return validateAuthorization

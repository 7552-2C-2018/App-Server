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
            return Responses.unauthorized('FacebookId not found')
        token = request.headers.get('access-token')

        if token != user['token']:
            return Responses.unauthorized('Invalid token')

        current_date_seconds = time.mktime(datetime.datetime.utcnow().timetuple())
        exp_date_seconds = time.mktime(user['exp_date'].timetuple())
        if current_date_seconds > exp_date_seconds:
            return Responses.unauthorized('Expirated token')

        return function(*args, **kwargs)

    return validateAuthorization

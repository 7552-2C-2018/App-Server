from functools import wraps
from apis import api
from flask import request

from Structures.Response import Responses
from DatabaseComunnication.UserTransactions import UserTransactions


def validateAuth(function):

    @wraps(function)
    def validateAuthorization(*args, **kwargs):

        user = findUserById(requests.headers.get('facebookId'))

        if user is None:
            return Responses.unauthorized('FacebookId not found')
        token = request.headers.get('token')

        if token != user['token']:
            return Responses.unauthorized('Invalid token')

        return function (*args, **kwargs)

    return validateAuthorization

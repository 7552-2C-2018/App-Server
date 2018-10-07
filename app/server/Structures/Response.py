from flask import jsonify


class Responses:
    
    def __init__(self):
        pass

    @staticmethod
    def __jsonifyResponse(message="", data=None, status=""):
        response = {'status': status, 'data': data, 'message': message}
        return jsonify(response)

    @staticmethod
    def success(message = '', data = None):
        return Responses.__jsonifyResponse(message, data, 200)

    @staticmethod
    def created(message='', data=None):
        return Responses.__jsonifyResponse(message, data, 201)

    @staticmethod
    def badRequest(message='', data=None):
        return Responses.__jsonifyResponse(message, data, 400)

    @staticmethod
    def unauthorized(message='', data=None):
        return Responses.__jsonifyResponse(message, data, 401)

    @staticmethod
    def notFound(message='', data=None):
        return Responses.__jsonifyResponse(message, data, 404)

    @staticmethod
    def internalServerError(message='', data=None):
        return Responses.__jsonifyResponse(message, data, 500)

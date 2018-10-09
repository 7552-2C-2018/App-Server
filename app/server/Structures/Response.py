responses = {
        200: 'Success',
        201: 'Created',
        400: 'BadRequest',
        401: 'Unauthorized',
        404: 'NotFound',
        500: 'InternalServerError',
    }
class Responses:
    
    def __init__(self):
        pass

    @staticmethod
    def __parseResponse(message="", data=None, status=""):
        response = {'status': status, 'data': data, 'message': message}
        return response

    @staticmethod
    def success(message = '', data = None):
        return Responses.__parseResponse(message, data, 200)

    @staticmethod
    def created(message='', data=None):
        return Responses.__parseResponse(message, data, 201)

    @staticmethod
    def badRequest(message='', data=None):
        return Responses.__parseResponse(message, data, 400)

    @staticmethod
    def unauthorized(message='', data=None):
        return Responses.__parseResponse(message, data, 401)

    @staticmethod
    def notFound(message='', data=None):
        return Responses.__parseResponse(message, data, 404)

    @staticmethod
    def internalServerError(message='', data=None):
        return Responses.__parseResponse(message, data, 500)

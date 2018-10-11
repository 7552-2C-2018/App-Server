from flask_restplus import Resource,Api, reqparse, Namespace
from server.services.userServices import UserServices
from server.services.Validator.validateAuth import validateAuth
from server.Structures.Response import responses

api = Namespace('users', description='Melli user-related endpoints')

login = reqparse.RequestParser()
login.add_argument('facebookId', type=str, help='facebookId', location='headers', required=True)
login.add_argument('token', type=str, help='token fb', location='headers', required=True)

register = login.copy()
register.add_argument('firstName', type=str, help='nombre', location='form', required=True)
register.add_argument('lastName', type=str, help='apellido', location='form', required=True)
register.add_argument('photoUrl', type=str, help='foto', location='form', required=True)
register.add_argument('email', type=str, help='mail', location='form', required=True)

update = login.copy()
update.add_argument('firstName', type=str, help='nombre', location='form')
update.add_argument('lastName', type=str, help='apellido', location='form')
update.add_argument('photoUrl', type=str, help='foto', location='form')
update.add_argument('email', type=str, help='mail', location='form')



@api.route('/')
class LoginValidator(Resource):
    @api.doc(responses=responses)
    @api.expect(login)
    def get(self):
        return_data = UserServices.checkLogin(login.parse_args())
        return return_data["data"], return_data["status"], {'message': return_data["message"]}
        
    @api.doc(responses=responses)
    @api.expect(register)
    def post(self):
        return_data = UserServices.registerUser(register.parse_args())
        return return_data["data"], return_data["status"], {'message': return_data["message"]}

    @api.doc(responses=responses)
    @api.expect(update)
    @validateAuth
    def put(self):
        return_data = UserServices.updateUser(update.parse_args())
        return return_data["data"], return_data["status"], {'message': return_data["message"]}

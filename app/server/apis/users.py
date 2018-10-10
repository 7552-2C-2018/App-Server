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


@api.doc(responses=responses)
@api.route('/')
class LoginValidator(Resource):

    @api.expect(login)
    def get(self):
        return_data = UserServices.checkLogin(login.parse_args())
        return {'message': return_data["message"]}, return_data["status"], {'body': return_data["data"]}

    @api.expect(register)
    def post(self):
        return UserServices.registerUser(register.parse_args())

    @api.expect(update)
    @validateAuth
    def put(self):
        return UserServices.updateUser(update.parse_args())

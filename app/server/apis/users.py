import time

from flask_restplus import Resource, Api, reqparse, Namespace

from server.services.Monitoring.monitor import monitor
from server.services.userServices import UserServices
from server.services.Validator.validateAuth import validateAuth
from server.Structures.Response import responses

api = Namespace('users', description='Melli user-related endpoints')

path = 'users/'

common_args = reqparse.RequestParser()
common_args.add_argument('facebookId', type=str, help='facebookId', location='headers', required=True)

login = reqparse.RequestParser()
login.add_argument('token', type=str, help='token de acceso de facebook', location='headers', required=True)

register = login.copy()
register.add_argument('firstName', type=str, help='nombre', location='form', required=True)
register.add_argument('lastName', type=str, help='apellido', location='form', required=True)
register.add_argument('photoUrl', type=str, help='foto', location='form', required=True)
register.add_argument('email', type=str, help='mail', location='form', required=True)

update = common_args.copy()
update.add_argument('token', type=str, help='token de acceso', location='headers', required=True)
update.add_argument('firstName', type=str, help='nombre', location='form')
update.add_argument('lastName', type=str, help='apellido', location='form')
update.add_argument('photoUrl', type=str, help='foto', location='form')
update.add_argument('email', type=str, help='mail', location='form')


@api.route('/login')
class LoginValidator(Resource):
    @api.doc(responses=responses)
    @api.expect(login)
    def get(self):
        """Login credentials validation endpoint"""
        time_start = time.time()
        return_data = UserServices.checkLogin(login.parse_args())
        time_end = time.time()
        monitor(time_start, time_end, path, "get")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/register')
class RegisterValidator(Resource):
    @api.doc(responses=responses)
    @api.expect(register)
    def post(self):
        """Registering user endpoint"""
        time_start = time.time()
        return_data = UserServices.registerUser(register.parse_args())
        time_end = time.time()
        monitor(time_start, time_end, path, "post")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/')
class RegisterValidator(Resource):
    @api.doc(responses=responses)
    @api.expect(update)
    @validateAuth
    def put(self):
        """Updating user data endpoint"""
        time_start = time.time()
        return_data = UserServices.updateUser(update.parse_args())
        time_end = time.time()
        monitor(time_start, time_end, path, "put")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/activities')
class Activities(Resource):
    @api.doc(responses=responses)
    @api.expect(common_args)
    def get(self):
        """Login credentials validation endpoint"""
        time_start = time.time()
        return_data = UserServices.getActivities(common_args.parse_args())
        time_end = time.time()
        monitor(time_start, time_end, path, "get")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}

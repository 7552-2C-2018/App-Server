import json
from flask import request
from flask_restplus import Resource, reqparse, Namespace
from server.services.userServices import UserServices
from server.services.Validator.validateAuth import validateAuth

api = Namespace('users', description='Melli user-related endpoints')

login = api.parser()
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
    @api.doc(endpoint="Login endpoint")
    @api.expect(login)
    def get(self):
        return UserServices.checkLogin(login.parse_args())

    @api.doc(endpoint="User registration endpoint")
    @api.expect(register)
    def post(self):
        return UserServices.registerUser(register.parse_args())

    @api.doc(endpoint="User datas update endpoint")
    @api.expect(update)
    @validateAuth
    def put(self):
        return UserServices.updateUser(update.parse_args())

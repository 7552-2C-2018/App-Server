from flask import Flask, request, jsonify
from flask_restplus import Resource, Api, reqparse
from . import app
import json
import requests
import jwt
import datetime
api = Api(app, version='0.1', title='Our sample API',description='This is our sample API',)

colleccion_prueba = app.database.prueba

@api.route('/welcome')
class Hello(Resource):
	def get(self):
		return {'welcome': "I'm the App Server for Melli"}

parser = api.parser()
parser.add_argument('facebookId', type=str, help='Some param', location='data')
parser.add_argument('firstName', type=str, help='Some param', location='data')
parser.add_argument('lastName', type=str, help='Some param', location='data')
parser.add_argument('photoUrl', type=str, help='Some param', location='data')
parser.add_argument('photoUrl', type=str, help='Some param', location='data')
parser.add_argument('email', type=str, help='Some param', location='data')
parser.add_argument('token', type=str, help='Some param', location='data')
@api.route('/login')
class LoginValidator(Resource):
	@staticmethod
	def missingValues(data):
		if all (k in data for k in ("facebookId","firstName","lastName","photoUrl","email","token")):
			return False
		return True
	@api.doc(parser=parser)
	def post(self):
		request_data = request.form
		response = {}
		if self.missingValues(request_data):
			status = 400
			message = "Faltan datos en la llamada"
		else:
			url = 'https://graph.facebook.com/me?access_token=' + request_data["token"]
			r = requests.get(url)
			print(r.status_code)
			print(r.text)
			if (r.status_code == 200):
				output = json.loads(r.text)
				if (output["id"] == request_data["facebookId"]):
					status = 200
					payload = {"user": output["id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=900)}
					token = jwt.encode(payload, app.config.get('SECRET_KEY'))
					print(token.decode('UTF-8'))
					message = "Token generado correctamente"
					response['token'] = token.decode('UTF-8')
				else:
					status = 401
					message = "El facebook ID es invalido"
			else:
				status = 401
				message = "El access_token es invalido"
		response['status'] = status
		response['message'] = message
		return json.dumps(response)

if __name__ == '__main__':
	app.run()
from flask_restplus import Namespace, Resource, fields

api = Namespace('ping', description='Melli ping endpoint')

@api.route('/')
class Hello(Resource):
	def get(self):
		return {'ping': "pong"}



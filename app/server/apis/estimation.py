import time

from flask_restplus import Resource, Namespace, reqparse

from server.Communication.SharedServerCommunication.sharedServerRequests import SharedServerRequests
from server.Structures.Response import responses
from server.services.Monitoring.monitor import monitor
from server.services.Validator.validateAuth import validateAuth

api = Namespace('estimation', description='Melli estimation-related endpoints')

path = 'estimation/'

parser = reqparse.RequestParser()
parser.add_argument('facebookId', type=str, help='facebookId', location='headers')
parser.add_argument('token', type=str, help='Token de acceso', location='headers')


@api.doc(responses=responses)
@api.route('/')
class Estimation(Resource):
	@api.expect(parser)
	@validateAuth
	def get(self):
		"""Endpoint that gets all Categories"""
		time_start = time.time()
		data = parser.parse()
		return_data = SharedServerRequests.calculateShipping(data)
		time_end = time.time()
		monitor(time_start, time_end, path, "get")
		return return_data["data"], return_data["status"], {'message': return_data["message"]}


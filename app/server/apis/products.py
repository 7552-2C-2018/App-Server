import time

from flask_restplus import Resource, Api, Namespace, reqparse

from server.services.Monitoring.monitor import monitor
from server.services.productServices import ProductServices
from server.services.Validator.validateAuth import validateAuth
from server.Structures.Response import responses

api = Namespace('products', description='Melli post-related endpoints')

path = 'products/'

parser = reqparse.RequestParser()
parser.add_argument('facebookId', type=str, help='facebookId', location='headers')
parser.add_argument('token', type=str, help='Token de acceso', location='headers')


@api.doc(responses=responses)
@api.route('/categories')
class Categories(Resource):
	@api.expect(parser)
	@validateAuth
	def get(self):
		"""Endpoint that gets all Categories"""
		time_start = time.time()
		return_data = ProductServices.get_categories()
		time_end = time.time()
		monitor(time_start, time_end, path, "get")
		return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.doc(responses=responses)
@api.route('/payments')
class Payments(Resource):
	@api.expect(parser)
	@validateAuth
	def get(self):
		"""Endpoint that gets all Payments types"""
		time_start = time.time()
		return_data = ProductServices.get_payments()
		time_end = time.time()
		monitor(time_start, time_end, path, "get")
		return return_data["data"], return_data["status"], {'message': return_data["message"]}

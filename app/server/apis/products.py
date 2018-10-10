from flask_restplus import Resource, Api, Namespace, reqparse
from server.services.productServices import ProductServices
from server.services.Validator.validateAuth import validateAuth
from server.Structures.Response import responses

api = Namespace('products', description='Melli post-related endpoints')

parser = reqparse.RequestParser()
parser.add_argument('facebookId', type=str, help='facebookId', location='headers')
parser.add_argument('access-token', type=str, help='Token de acceso', location='headers')


@api.doc(responses=responses)
@api.route('/categories')
class Categories(Resource):
	@api.expect(parser)
	@validateAuth
	def get(self):
		return_data = ProductServices.get_categories()
		return return_data["data"], return_data["status"], {'message': return_data["message"]}

@api.doc(responses=responses)
@api.route('/payments')
class Payments(Resource):
	@api.expect(parser)
	@validateAuth
	def get(self):
		return_data = ProductServices.get_payments()
		return return_data["data"], return_data["status"], {'message': return_data["message"]}


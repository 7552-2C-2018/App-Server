import json
from flask import request
import jwt
import datetime
from flask import Flask, jsonify
from flask_restplus import Resource, Api, Namespace, reqparse
from server.services.productServices import ProductServices
from server.services.Validator.validateAuth import validateAuth

api = Namespace('products', description='Melli post-related endpoints')

parser = reqparse.RequestParser()
parser.add_argument('facebookId', type=str, help='facebookId', location='headers')
parser.add_argument('access-token', type=str, help='Token de acceso', location='headers')

@api.route('/categories')
class Categories(Resource):
	@api.expect(parser)
	@validateAuth
	def get(self):
		return ProductServices.getCategories()


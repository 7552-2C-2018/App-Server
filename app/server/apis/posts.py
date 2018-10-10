import json
import requests
import jwt
import datetime
from flask import Flask, jsonify
from flask_restplus import Resource, Api, Namespace, reqparse
from server.services.Validator.validateAuth import validateAuth
from server.services.postServices import PostServices
from server.Structures.Response import responses

api = Namespace('posts', description='Melli post-related endpoints')

common_args = reqparse.RequestParser()
common_args.add_argument('facebookId', type=str, help='facebookId', location='headers')
common_args.add_argument('access-token', type=str, help='Token de acceso', location='headers')

get_product = common_args.copy()

new_post_args = common_args.copy()
new_post_args.add_argument('title', type=str, help='titulo del post', location='form', required=True)
new_post_args.add_argument('desc', type=str, help='descripcion del post', location='form', required=True)
new_post_args.add_argument('stock', type=int, help='stock del post', location='form', required=True)
new_post_args.add_argument('payments', type=list, help='tipos de pago', location='form', required=True)
new_post_args.add_argument('email', type=str, help='mail', location='form', required=True)

update_post_args = common_args.copy()
update_post_args.add_argument('title', type=str, help='titulo del post', location='form')
update_post_args.add_argument('desc', type=str, help='descripcion del post', location='form')
update_post_args.add_argument('stock', type=int, help='stock del post', location='form')
update_post_args.add_argument('payments', type=list, help='tipos de pago', location='form')
update_post_args.add_argument('email', type=str, help='mail', location='form')

@api.doc(responses=responses)
@api.route('/')
class NewPost(Resource):

	@api.expect(common_args)
	@validateAuth
	def get(self):
		return_data = PostsServices.get_all_posts(common_args.parse_args())
		return {'message': return_data["message"]}, return_data["status"], {'body': return_data["data"]}

	@api.expect(common_args)
	@api.param('product_id', 'id del producto requerido')
	@validateAuth
	def get(self):
		return_data = PostsServices.get_post(common_args.parse_args())
		return {'message': return_data["message"]}, return_data["status"], {'body': return_data["data"]}

	@api.expect(new_post_args)
	@validateAuth
	def post(self):
		return PostsServices.new_post(register.parse_args())

	@api.expect(update_post_args)
	@validateAuth
	def put(self):
		return UserServices.updateUser(update.parse_args())


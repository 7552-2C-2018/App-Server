import json
import requests
import jwt
import datetime
from flask import Flask, jsonify
from flask_restplus import Resource, Api, Namespace, reqparse
from server.services.Validator.validateAuth import validateAuth

api = Namespace('posts', description='Melli post-related endpoints')

common_args = reqparse.RequestParser()
common_args.add_argument('facebookId', type=str, help='facebookId', location='headers')
common_args.add_argument('access-token', type=str, help='Token de acceso', location='headers')

new_post_args = common_args.copy()
new_post_args.add_argument('title', type=str, help='titulo del post', location='form')
new_post_args.add_argument('desc', type=str, help='descripcion del post', location='form')
new_post_args.add_argument('stock', type=int, help='stock del post', location='form')
new_post_args.add_argument('payments', type=list, help='tipos de pago', location='form')
new_post_args.add_argument('email', type=str, help='mail', location='body')


@api.route('/newPost')
class NewPost(Resource):
	@validateAuth
	@api.expect(new_post_args)
	def post(self):
		return jsonify("")


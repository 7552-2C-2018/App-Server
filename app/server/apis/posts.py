import json
import requests
import jwt
import datetime
from flask import Flask, jsonify
from flask_restplus import Resource, Api, Namespace, reqparse

api = Namespace('posts', description='Melli post-related endpoints')

parser = reqparse.RequestParser()
parser.add_argument('facebookId', type=str, help='facebookId', location='body')
parser.add_argument('title', type=str, help='titulo del post', location='body')
parser.add_argument('desc', type=str, help='descripcion del post', location='body')
parser.add_argument('stock', type=str, help='stock del post', location='body')
parser.add_argument('payments', type=str, help='tipos de pago', location='body')
parser.add_argument('email', type=str, help='mail', location='body')
parser.add_argument('token', type=str, help='token fb', location='body')


@api.route('/newPost')
class NewPost(Resource):
	#@validateAuth
	@api.expect(parser)
	def post(self):
		return jsonify("")


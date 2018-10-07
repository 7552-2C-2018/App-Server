import os
from dotenv import load_dotenv, find_dotenv
from flask_pymongo import PyMongo
from werkzeug.contrib.fixers import ProxyFix


class Config(object):

	@staticmethod
	def set_up_env(app):
		load_dotenv(find_dotenv())
		app.wsgi_app = ProxyFix(app.wsgi_app)
		app.config['SECRET_KEY'] = 'Taller2C2018'

	@staticmethod
	def set_up_mongodb(app):
		# Mongo DB config
		MONGO_URL = os.environ.get('MONGO_URL')
		if not MONGO_URL:
			MONGO_URL = 'mongodb://database:27017/app-server'
		app.config['MONGO_URI'] = MONGO_URL
		return PyMongo(app)

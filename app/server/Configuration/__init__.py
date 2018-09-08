import os
from dotenv import load_dotenv, find_dotenv
from flask_pymongo import PyMongo
class Config(object):
	@staticmethod
	def set_up_env():
		load_dotenv(find_dotenv())
	@staticmethod
	def set_up_mongodb(app):
		# Mongo DB config
		MONGO_URL = os.environ.get('MONGO_URL')
		if not MONGO_URL:
			MONGO_URL = 'mongodb://database:27017/app-server'
		app.config['MONGO_URI'] = MONGO_URL
		return PyMongo(app)
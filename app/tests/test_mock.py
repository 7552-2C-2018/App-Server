# content of test_mock.py
import pytest
from flask_pymongo import PyMongo
from flask import Flask
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://admin:Taller2018@ds245532.mlab.com:45532/app-server'
with app.app_context():
    app.database = PyMongo(app).db
def test_mock():
	assert 1==1

def test_db():
	assert app.database.prueba.findone() is not None
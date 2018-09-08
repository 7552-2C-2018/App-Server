from flask import Flask
from flask_cors import CORS
from server.Configuration import Config

app = Flask(__name__)
CORS(app)
Config().set_up_env()

mongodb = Config().set_up_mongodb(app)

with app.app_context():
    app.database = mongodb.db
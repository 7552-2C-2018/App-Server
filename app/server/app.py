from flask import Flask
from flask_restplus import Resource, Api, reqparse
from . import app
from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, 
          version='0.1', 
          title='Our sample API',
          description='This is our sample API',
)
colleccion_prueba = app.database.prueba

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}



@api.route('/login')
class HelloWorld(Resource):
    def get(self):
    	return colleccion_prueba.find_one({'hello': 'world'}, {'_id': 0})

if __name__ == '__main__':
    app.run()

from flask import Flask
from flask import request
import json

app = Flask(__name__)


@app.route('/')
def hello():
    return "I'm the App Server for Melli"

@app.route('/login', methods=['POST'])
def user_login():
	request_data = request.get_json()
	if missingValues(request_data):
		response = {'status': 400, 'message': 'Input incorreto'}
	else:
		response = {'status': 200, 'message': 'Input OK'}

	return json.dumps(response)

def missingValues(data):
	if all (k in foo for k in ("facebookId","firstName","lastName","photoUrl","email","token")):
		return true
	return false

if __name__ == '__main__':
    app.run(host='0.0.0.0')
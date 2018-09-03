
from flask import Flask
from flask import request
import json
import requests
import jwt
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ImAverySecureScretKey'


@app.route('/')
def hello():
    return "I'm the App Server for Melli"

@app.route('/login', methods=['POST'])
def user_login():
	request_data = request.get_json()
	response = {}
	if missingValues(request_data):
		status = 400
		message = "Faltan datos en la llamada"
	else:
		url = 'https://graph.facebook.com/me?access_token=' + request_data["token"]
		r = requests.get(url)
		print(r.status_code)
		print(r.text)
		if (r.status_code == 200):
			output = json.loads(r.text)
			if (output["id"] == request_data["facebookId"]):
				status = 200
				payload = {"user": output["id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=900)}
				token = jwt.encode(payload, app.config.get('SECRET_KEY'))
				print(token.decode('UTF-8'))
				message = "Token generado correctamente"
				response['token'] = token.decode('UTF-8')
			else:
				status = 401
				message = "El facebook ID es invalido"
		else:
			status = 401
			message = "El access_token es invalido"
	response['status'] = status
	response['message'] = message
	return json.dumps(response)

def missingValues(data):
	if all (k in data for k in ("facebookId","firstName","lastName","photoUrl","email","token")):
		return False
	return True

if __name__ == '__main__':
    app.run(host='0.0.0.0')
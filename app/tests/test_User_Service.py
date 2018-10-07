# content of test_mock.py
import pytest
from server.services.userServices import UserServices
from server.setup import app
with app.app_context():
	db = app.database
	invalid_request = {"facebookId": "", "token": ""}
	userServ = UserServices()


def test_login_invalid_facebook_id():
	response = userServ.checkLogin(invalid_request)
	assert response["status"] == 400
	assert response["message"] == 'FacebookId Invalido'

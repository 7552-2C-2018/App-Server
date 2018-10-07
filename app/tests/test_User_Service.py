# content of test_mock.py
import pytest
from server.services.userServices import UserServices

invalid_request = {"facebookId": "a", "token": ""}

def test_login_invalid_facebook_id():
	response = UserServices.checkLogin(invalid_request)
	assert response["status"] == 400
	assert response["message"] == 'FacebookId Invalido'

def test_db():
	assert app.database.prueba.find() is not None
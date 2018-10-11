from . import GenericTest
from server.setup import app
from server.services.userServices import UserServices
from unittest.mock import *



class UserTests(GenericTest):

    def test_login_invalid_facebook_id(self):
        invalid_request = {"facebookId": "", "token": ""}
        response = UserServices.checkLogin(invalid_request)
        assert response["status"] == 400
        assert response["message"] == 'FacebookId Invalido'

    @patch('server.Communication.facebookCommunication.FacebookCommunication.ValidateUser', MagicMock(return_value=True))
    def test_login_unregistered_id(self):
        invalid_request = {"facebookId": "", "token": ""}
        response = UserServices.checkLogin(invalid_request)
        assert response["status"] == 401
        assert response["message"] == 'Usuario no registrado'
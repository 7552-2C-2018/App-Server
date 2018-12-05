from . import GenericTest
from server.setup import app
from server.services.userServices import UserServices
from unittest.mock import *
invalid_fb_credentials = {"facebookId": "", "token": ""}
registered_credentials = {"facebookId": "102510700706099", "token": ""}


mark_credentials = {"facebookId": "102510700706087",
                    "token": "token",
                    "firstName": "mark",
                    "lastName": "zuc",
                    "photoUrl": "foto",
                    "email": "mail"}
mark_updated_credentials = {"facebookId": "102510700706099",
                    "token": "token",
                    "firstName": "Mark",
                    "lastName": "zucer",
                    "photoUrl": "foto2",
                    "email": "mailNuevo"}


class UserTests(GenericTest):

    def test_login_invalid_fb_credentials(self):
        response = UserServices.checkLogin(invalid_fb_credentials)
        assert response["status"] == 400
        assert response["message"] == 'FacebookId Invalido'

    @patch('server.Communication.facebookCommunication.FacebookCommunication.ValidateUser',
           MagicMock(return_value=True))
    def test_login_unregistered_id(self):
        response = UserServices.checkLogin(invalid_fb_credentials)
        assert response["status"] == 400
        assert response["message"] == 'Usuario no registrado'

    def test_register_invalid_facebook_id(self):
        response = UserServices.registerUser(invalid_fb_credentials)
        assert response["status"] == 400
        assert response["message"] == 'FacebookId Invalido'

    @patch('server.Communication.facebookCommunication.FacebookCommunication.ValidateUser',
           MagicMock(return_value=True))
    def test_register_new_user(self):
        response = UserServices.registerUser(mark_credentials)
        assert response["status"] == 201
        assert response["message"] == 'Usuario registrado correctamente'

    @patch('server.Communication.facebookCommunication.FacebookCommunication.ValidateUser',
           MagicMock(return_value=True))
    def test_update_data_unregistered_user(self):
        response = UserServices.updateUser(invalid_fb_credentials)
        assert response["status"] == 400
        assert response["message"] == 'Usuario no registrado'

    @patch('server.Communication.facebookCommunication.FacebookCommunication.ValidateUser',
           MagicMock(return_value=True))
    def test_update_data_user(self):
        response = UserServices.updateUser(mark_updated_credentials)
        assert response["status"] == 200
        assert response["message"] == 'Usuario actualizado correctamente'

    @patch('server.Communication.facebookCommunication.FacebookCommunication.ValidateUser',
           MagicMock(return_value=True))
    def test_login_registered_id(self):
        response = UserServices.checkLogin(registered_credentials)
        assert response["status"] == 200
        assert response["message"] == 'Token generado correctamente'
        assert response["data"] != ''


from . import GenericTest
from server.setup import app
from server.services.userServices import UserServices


class UserTests(GenericTest):

    def test_login_invalid_facebook_id(self):
        invalid_request = {"facebookId": "", "token": ""}
        response = UserServices.checkLogin(invalid_request)
        assert response["status"] == 400
        assert response["message"] == 'FacebookId Invalido'

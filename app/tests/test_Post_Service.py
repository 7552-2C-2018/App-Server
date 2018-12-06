from . import GenericTest
from server.setup import app
from server.services.postServices import PostServices
from unittest.mock import *

registered_credentials = {"facebookId": "102510700706087", "token": ""}
registered_credentials_with_date = {"facebookId": "102510700706087", "token": "", "postId": "1025107007060871539228792"}
new_post = {"facebookId": "102510700706087",
            "category": "test",
            "coordenates": [
                12,
                13
            ],
            "description": "Desde swagger",
            "new": True,
            "payments": [
                "EFECTIVO"
            ],
            "pictures": None,
            "price": 10,
            "shipping": False,
            "stock": 2,
            "title": "Prueba"}

@patch('server.Communication.FirebaseCommunication.firebaseCommunication.'
       'FirebaseCommunication.send_notification', MagicMock())
class PostsTests(GenericTest):

    def test_get_all_posts(self):
        response = PostServices.getAllPosts(registered_credentials)
        assert response["status"] == 200
        assert response["message"] == 'Post obtenidos satisfactoriamente'

    def test_get_post_id(self):
        response = PostServices.getPost(registered_credentials_with_date)
        assert response["status"] == 200
        assert response["message"] == 'Post obtenidos satisfactoriamente'

    def test_new_post_id(self):
        response = PostServices.createNewPost(new_post)
        assert response["status"] == 201
        assert response["message"] == 'Post creado satisfactoriamente'

from . import GenericTest
from server.setup import app
from server.services.postServices import PostServices
from unittest.mock import *

registered_credentials = {"facebookId": "102510700706087", "token": ""}
registered_credentials_with_date = {"facebookId": "102510700706087", "token": "", "publ_date": "1539228792"}

class PostsTests(GenericTest):

    def test_get_all_posts(self):
     response = PostServices.getAllPosts(registered_credentials)
     assert response["status"] == 200
     assert response["message"] == 'Productos obtenidos satisfactoriamente'

    def test_get_post_id(self):
        response = PostServices.getAllPosts(registered_credentials_with_date)
        assert response["status"] == 200
        assert response["message"] == 'Productos obtenidos satisfactoriamente'
#     def test_getAllPosts(request_data):
#         response = PostServices.getAllPosts()
#         assert response["status"] == 200
#         assert response["message"] == 'Productos obtenidos satisfactoriamente'
#
#
#         response = PostTransactions.findPostById(request_data["facebookId"],int(request_data["publDate"]))
#         if not response is None:
#             response["name"] = UserTransactions.getUserName(request_data["facebookId"])
#             return Responses.success('Productos obtenidos satisfactoriamente', response)
#         else:
#             return Responses.badRequest('Post inexistente')

#     def test_getPostInexistente(self):
#
from . import GenericTest
from server.setup import app
from server.services.postServices import PostServices
from unittest.mock import *


# class UserTests(GenericTest):
#     def test_getPostInexistente(self):
#
#     def createNewPost(self):
#         PostTransactions.newPost(request_data)
#         return Responses.created('Productos creados satisfactoriamente', "")
#
#     def test_new_post(self):
#         response = UserServices.checkLogin(invalid_fb_credentials)
#         assert response["status"] == 400
#         assert response["message"] == 'FacebookId Invalido'
#
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


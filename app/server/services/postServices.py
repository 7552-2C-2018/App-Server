from server.Structures.Response import Responses
from server.Communication.DatabaseCommunication.postTransactions import PostTransactions
from server.Communication.DatabaseCommunication.userTransactions import UserTransactions
import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

class PostServices:

    def __init__(self):
        pass

    @staticmethod
    def getAllPosts(request_data):
        response = PostTransactions.getPosts(request_data)
        return Responses.success('Post obtenidos satisfactoriamente', response)

    @staticmethod
    def getPost(request_data):
        response = PostTransactions.find_post_by_post_id(request_data["postId"])

        if not response is None:
            response["name"] = UserTransactions.getUserName(response["_id"]["facebookId"])
            return Responses.success('Post obtenidos satisfactoriamente', response)
        else:
            return Responses.badRequest('Post inexistente')

    @staticmethod
    def getPostByUser(request_data):
        response = PostTransactions.find_post_by_user_id(request_data["userId"])

        if not response is None:
            return Responses.success('Post obtenidos satisfactoriamente', response)
        else:
            return Responses.badRequest('Usuario sin Posts')

    @staticmethod
    def createNewPost(request_data):
        PostTransactions.new_post(request_data)
        return Responses.created('Post creado satisfactoriamente', "")

    @staticmethod
    def updatePost(request_data):
        response = PostTransactions.update_post_data(request_data)
        if response != "Estado Invalido":
            return Responses.success('Post actualizado satisfactoriamente', "")
        else:
            return Responses.badRequest('Estado Invalido')

from server.Structures.Response import Responses
from server.Communication.DatabaseCommunication.postTransactions import PostTransactions
from server.Communication.DatabaseCommunication.userTransactions import UserTransactions
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


class PostServices:

    @staticmethod
    def getAllPosts(request_data):
        response = PostTransactions.getPosts()
        return Responses.success('Productos obtenidos satisfactoriamente', response)

    @staticmethod
    def getPost(request_data):
        response = PostTransactions.findPostById(request_data["postId"])

        if not response is None:
            response["name"] = UserTransactions.getUserName(response["_id"]["facebookId"])
            return Responses.success('Productos obtenidos satisfactoriamente', response)
        else:
            return Responses.badRequest('Post inexistente')

    @staticmethod
    def getPostByUser(request_data):
        response = PostTransactions.findPostByUserId(request_data["userId"])

        if not response is None:
            return Responses.success('Productos obtenidos satisfactoriamente', response)
        else:
            return Responses.badRequest('Usuario sin Posts')

    @staticmethod
    def createNewPost(request_data):
        PostTransactions.newPost(request_data)
        return Responses.created('Producto creado satisfactoriamente', "")

    @staticmethod
    def updatePost(request_data):
        return Responses.badRequest('FacebookId Invalido')


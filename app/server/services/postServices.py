from server.Structures.Response import Responses
from server.Communication.DatabaseCommunication.postTransactions import PostTransactions
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


class PostServices:

    @staticmethod
    def getAllPosts(request_data):
        response = PostTransactions.getPosts()
        return Responses.success('Productos obtenidos satisfactoriamente', response)

    @staticmethod
    def getPost(request_data):
        response = PostTransactions.findPostById(request_data["post_id"])
        return Responses.success('Productos obtenidos satisfactoriamente', response)

    @staticmethod
    def createNewPost(request_data):
        response = PostTransactions.newPost(request_data["facebookId"], request_data["title"],
                                 request_data["desc"], request_data["stock"], request_data["payments"], request_data["email"])
        return Responses.success('Productos obtenidos satisfactoriamente', response)

    @staticmethod
    def updatePost(request_data):
        return Responses.badRequest('FacebookId Invalido')


from server.Communication.DatabaseCommunication.postTransactions import PostTransactions
from server.Communication.DatabaseCommunication.questionTransactions import QuestionTransactions
from server.Communication.DatabaseCommunication.userTransactions import UserTransactions
from server.Communication.FirebaseCommunication.firebaseCommunication import FirebaseCommunication
from server.Structures.Response import Responses
import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

class QuestionServices:

    def __init__(self):
        pass

    @staticmethod
    def getAllQuestions(postId):
        response = QuestionTransactions.getQuestions(postId)
        return Responses.success('Preguntas obtenidas satisfactoriamente', response)

    @staticmethod
    def getQuestion(request_data):
        response = QuestionTransactions.findQuestion(request_data["questionId"])
        if not response is None:
            return Responses.success('Pregunta obtenida satisfactoriamente', response)
        else:
            return Responses.badRequest('Pregunta inexistente')

    @staticmethod
    def createNewQuestion(request_data):
        post_data = PostTransactions.find_post_by_post_id(request_data["postId"])
        if post_data is None:
            return Responses.badRequest('Post inexistente', "")
        QuestionTransactions.newQuestion(request_data)
        UserTransactions.pushUserActivitiy(request_data["facebookId"], "question")
        UserTransactions.pushUserActivitiy(post_data["_id"]["facebookId"], "questioned")
        QuestionServices.__sendNotifications(request_data)
        FirebaseCommunication.send_notification(request_data["facebookId"],
                                                "questioned",
                                                "Recibiste una pregunta sobre el post " + post_data["title"])
        return Responses.created('Pregunta creada satisfactoriamente', "")

    @staticmethod
    def updateQuestion(request_data):
        response = QuestionTransactions.updateQuestion(request_data)
        if response is not None:
            UserTransactions.pushUserActivitiy(request_data["facebookId"], "answer")
            UserTransactions.pushUserActivitiy(response["userId"], "answered")
            QuestionServices.__sendNotifications(request_data)
            return Responses.success('Pregunta actualizada satisfactoriamente', "")
        else:
            return Responses.badRequest('Pregunta inexistente', "")

    @staticmethod
    def __sendNotifications(data):
        pass


from server.Communication.DatabaseCommunication.questionTransactions import QuestionTransactions
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
        QuestionTransactions.newQuestion(request_data)
        return Responses.created('Pregunta creada satisfactoriamente', "")

    @staticmethod
    def updateQuestion(request_data):
        response = QuestionTransactions.updateQuestion(request_data)
        if response is not None:
            return Responses.success('Pregunta actualizada satisfactoriamente', "")

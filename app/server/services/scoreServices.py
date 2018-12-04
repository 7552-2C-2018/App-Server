from server.Communication.DatabaseCommunication.scoreTransactions import ScoreTransactions
from server.Structures.Response import Responses
from server.Communication.DatabaseCommunication.postTransactions import PostTransactions
from server.Communication.DatabaseCommunication.userTransactions import UserTransactions
import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG)


class ScoreServices:

    def __init__(self):
        pass

    @staticmethod
    def createNewScore(request_data):
        if request_data["rol"] in ["Comprador", "Vendedor"]:
            try:
                scored_user_id = ScoreTransactions.create_new_score(request_data)
            except Exception as e:
                logging.debug(str(e))
                return Responses.badRequest('Ya calificado', "")
            score_average = ScoreTransactions.find_scored_user_average(scored_user_id)
            UserTransactions.updateUserScorePoints(scored_user_id, score_average)
            return Responses.created('Calificado correctamente', "")

        else:
            return Responses.badRequest('Rol invalido')

    @staticmethod
    def getScore(request_data):
        response = ScoreTransactions.find_score(request_data)
        if response is not None:
            return Responses.success('Calificaciones obtenidas satisfactoriamente', response)
        else:
            return Responses.badRequest('El usuario no a calificado dicha compra')

    @staticmethod
    def getScoreByScorerId(request_data):
        response = ScoreTransactions.find_score_by_scorer_id(request_data["facebookId"])
        if response is not None:
            return Responses.success('Calificaciones obtenidas satisfactoriamente', response)
        else:
            return Responses.badRequest('Usuario sin scorees')

    @staticmethod
    def getScoreByScoredId(request_data):
        response = ScoreTransactions.find_score_by_scored_id(request_data["facebookId"])
        if response is not None:
            return Responses.success('Calificaciones obtenidas satisfactoriamente', response)
        else:
            return Responses.badRequest('Usuario sin scorees')

    @staticmethod
    def updateScore(request_data):
        response = ScoreTransactions.update_score(request_data)
        if response is not None:
            return Responses.success('Calificacion actualizada satisfactoriamente', "")
        else:
            return Responses.badRequest('Estado Invalido')



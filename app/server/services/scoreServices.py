import datetime
import time

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
                return Responses.internalServerError('Error al calificar', "")
            if scored_user_id == "Calificado":
                return Responses.badRequest('Ya calificado', "")
            if scored_user_id is None:
                return Responses.badRequest('No se puede calificar a si mismo', "")
            score_average = ScoreTransactions.find_scored_user_average(scored_user_id)
            UserTransactions.updateUserScorePoints(scored_user_id, score_average)
            UserTransactions.pushUserActivitiy(request_data["facebookId"], "scorer")
            UserTransactions.pushUserActivitiy(scored_user_id, "scored")
            return Responses.created('Calificado correctamente', "")

        else:
            return Responses.badRequest('Rol invalido')

    @staticmethod
    def getScore(request_data):
        response = ScoreTransactions.find_score(request_data)
        if response is not None:
            return Responses.success('Calificacion obtenida satisfactoriamente', response)
        else:
            return Responses.badRequest('El usuario no a calificado dicha compra')

    @staticmethod
    def getScoreByScorerId(request_data):
        response = ScoreTransactions.find_score_by_scorer_id(request_data["facebookId"])
        if response is not None:
            return Responses.success('Calificaciones obtenidas satisfactoriamente', response)
        else:
            return Responses.badRequest('Usuario sin scores')

    @staticmethod
    def getScoreByScoredId(request_data):
        response = ScoreTransactions.find_score_by_scored_id(request_data["facebookId"])
        if response is not None:
            return Responses.success('Calificaciones obtenidas satisfactoriamente', response)
        else:
            return Responses.badRequest('Usuario sin scores')

    @staticmethod
    def updateScore(request_data):
        scored_user_id = ScoreTransactions.update_score(request_data)
        if scored_user_id is None:
            return Responses.badRequest('Usuario sin scores para esa compra')
        try:
            score_average = ScoreTransactions.find_scored_user_average(scored_user_id)
            UserTransactions.updateUserScorePoints(scored_user_id, score_average)
            return Responses.success('Calificacion actualizada satisfactoriamente', "")
        except Exception as e:
            logging.debug(str(e))
            return Responses.badRequest('Error al actualizar los puntos', "")

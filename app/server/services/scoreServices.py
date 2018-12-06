from server.Communication.DatabaseCommunication.scoreTransactions import ScoreTransactions
from server.Communication.DatabaseCommunication.userTransactions import UserTransactions
from server.Communication.FirebaseCommunication.firebaseCommunication import FirebaseCommunication
from server.Structures.Response import Responses
from server.logger import Logger
LOGGER = Logger().get(__name__)


class ScoreServices:

    def __init__(self):
        pass

    @staticmethod
    def createNewScore(request_data):
        if request_data["rol"] in ["Comprador", "Vendedor"]:
            try:
                scored_user_id = ScoreTransactions.create_new_score(request_data)
            except Exception as e:
                LOGGER.error("No se pudo crear la calificacion! Error: " + str(e))
                return Responses.internalServerError('Error al calificar', "")
            if scored_user_id == "Calificado":
                LOGGER.warn("No se pudo crear la calificacion, ya existe")
                return Responses.badRequest('Ya calificado', "")
            if scored_user_id is None:
                LOGGER.warn("No se puede calificar a si mismo")
                return Responses.badRequest('No se puede calificar a si mismo', "")
            score_average = ScoreTransactions.find_scored_user_average(scored_user_id)
            UserTransactions.updateUserScorePoints(scored_user_id, score_average)
            UserTransactions.pushUserActivitiy(request_data["facebookId"], "Has calificado una publicacion")
            UserTransactions.pushUserActivitiy(scored_user_id, "Has sido calificado por una publicacion")
            FirebaseCommunication.send_notification(scored_user_id,
                                                    "Has recibido una calificacion: " + \
                                                    str(request_data["value"]) + " puntos.")
            return Responses.created('Calificado correctamente', "")
        else:
            LOGGER.warn("No se pudo crear la calificacion, Rol invalido")
            return Responses.badRequest('Rol invalido')

    @staticmethod
    def getScore(request_data):
        response = ScoreTransactions.find_score(request_data)
        if response is not None:
            return Responses.success('Calificacion obtenida satisfactoriamente', response)
        else:
            LOGGER.warn("El usuario no a calificado la compra")
            return Responses.badRequest('El usuario no a calificado dicha compra')

    @staticmethod
    def getScoreByScorerId(request_data):
        response = ScoreTransactions.find_score_by_scorer_id(request_data["facebookId"])
        if response is not None:
            return Responses.success('Calificaciones obtenidas satisfactoriamente', response)
        else:
            LOGGER.warn("El usuario no dio ninguna calificacion")
            return Responses.badRequest('Usuario sin scores')

    @staticmethod
    def getScoreByScoredId(request_data):
        response = ScoreTransactions.find_score_by_scored_id(request_data["facebookId"])
        if response is not None:
            return Responses.success('Calificaciones obtenidas satisfactoriamente', response)
        else:
            LOGGER.warn("El usuario no fue ninguna calificacion")
            return Responses.badRequest('Usuario sin scores')

    @staticmethod
    def updateScore(request_data):
        scored_user_id = ScoreTransactions.update_score(request_data)
        if scored_user_id is None:
            LOGGER.warn("El usuario no a calificado la compra")
            return Responses.badRequest('Usuario sin scores para esa compra')
        try:
            score_average = ScoreTransactions.find_scored_user_average(scored_user_id)
            UserTransactions.updateUserScorePoints(scored_user_id, score_average)
            return Responses.success('Calificacion actualizada satisfactoriamente', "")
        except Exception as e:
            LOGGER.error("No se pudo actualizar la calificacion! Error: " + str(e))
            return Responses.badRequest('Error al actualizar los puntos', "")

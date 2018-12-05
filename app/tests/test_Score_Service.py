import logging
from unittest.mock import *

from server.Communication.DatabaseCommunication.userTransactions import UserTransactions
from server.setup import app
from server.services.scoreServices import ScoreServices
from . import GenericTest

logging.basicConfig(filename='debug.log', level=logging.DEBUG)
buy_id_nuevo = "991539228999"
buy_id = "991539228792"
registered_credentials = {
    "facebookId": "102510700706087",
    "token": ""
}
registered_credentials_with_score = {
    "facebookId": "102510700706087",
    "token": "",
    "buyId": buy_id,
}
new_score_buyer = {
    "facebookId": "99",
    "buyId": buy_id_nuevo,
    "rol": "Comprador",
    "value": "2",
    "comment": "Mediocre"
}
new_score_seller = {
    "facebookId": "102510700706087",
    "buyId": buy_id_nuevo,
    "rol": "Vendedor",
    "value": "2",
    "comment": "Mediocre"
}
update_score = {
    "facebookId": "99",
    "buyId": buy_id,
    "value": "1",
    "comment": "Muy Mediocre"
}


@patch('server.Communication.FirebaseCommunication.firebaseCommunication.'
       'FirebaseCommunication.new_chat', MagicMock())
@patch('server.Communication.FirebaseCommunication.firebaseCommunication.'
       'FirebaseCommunication.send_notification', MagicMock())
class PostsTests(GenericTest):

    def test_get_all_given_scores(self):
        response = ScoreServices.getScoreByScorerId(registered_credentials)
        assert response["message"] == 'Calificaciones obtenidas satisfactoriamente'
        assert response["status"] == 200
        logging.debug(response["data"])
        assert response["data"] != ""

    def test_get_all_recived_scores(self):
        response = ScoreServices.getScoreByScoredId(registered_credentials)
        assert response["message"] == 'Calificaciones obtenidas satisfactoriamente'
        assert response["status"] == 200
        logging.debug(response["data"])
        assert response["data"] != ""

    def test_get_score(self):
        response = ScoreServices.getScore(registered_credentials_with_score)
        assert response["message"] == 'Calificacion obtenida satisfactoriamente'
        assert response["status"] == 200
        logging.debug(response["data"])
        assert response["data"] != ""

    def test_new_score_as_buyer(self):
        response = ScoreServices.createNewScore(new_score_buyer)
        assert response["message"] == 'Calificado correctamente'
        assert response["status"] == 201
        assert len(UserTransactions.getUserActivities(new_score_buyer["facebookId"])["activities"]) != 0
        assert len(UserTransactions.getUserActivities("102510700706087")) != 0

    def test_new_score_as_seller(self):
        response = ScoreServices.createNewScore(new_score_seller)
        assert response["message"] == 'Calificado correctamente'
        assert response["status"] == 201
        assert len(UserTransactions.getUserActivities(new_score_seller["facebookId"])["activities"]) != 0
        assert len(UserTransactions.getUserActivities("99")) != 0

    def test_update_score(self):
        response = ScoreServices.updateScore(update_score)
        assert response["message"] == 'Calificacion actualizada satisfactoriamente'
        assert response["status"] == 201
        logging.debug(str(UserTransactions.getUserActivities(update_score["facebookId"])))
        assert len(UserTransactions.getUserActivities(update_score["facebookId"])["activities"]) != 0

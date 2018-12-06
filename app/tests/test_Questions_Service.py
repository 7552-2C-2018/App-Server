import logging
from unittest.mock import *

from server.Communication.DatabaseCommunication.userTransactions import UserTransactions
from server.services.questionServices import QuestionServices
from server.setup import app
from . import GenericTest

with app.app_context():
    secret_key = app.config.get('SECRET_KEY')
logging.basicConfig(filename='debug.log', level=logging.DEBUG)
postId = "1025107007060871539228792"
questionId = "10251070070608715392287921999439"
registered_credentials = {
    "facebookId": "102510700706087",
    "token": ""
}
registered_credentials_with_question = {
    "facebookId": "102510700706087",
    "token": "",
    "questionId": questionId
}
new_question = {
    "facebookId": "99",
    "postId": postId,
    "question": "tenes stock?"
}
new_answer = {
    "facebookId": "99",
    "questionId": questionId,
    "respuesta": "tenes stock?"
}

@patch('server.Communication.FirebaseCommunication.firebaseCommunication.'
       'FirebaseCommunication.new_chat', MagicMock())
@patch('server.Communication.FirebaseCommunication.firebaseCommunication.'
       'FirebaseCommunication.send_notification', MagicMock())
class PostsQuestions(GenericTest):

    def test_get_all_questions(self):
        response = QuestionServices.getAllQuestions(postId)
        assert response["status"] == 200
        assert response["message"] == 'Preguntas obtenidas satisfactoriamente'

    def test_get_question_id(self):
        response = QuestionServices.getQuestion(registered_credentials_with_question)
        assert response["status"] == 200
        assert response["message"] == 'Pregunta obtenida satisfactoriamente'

    def test_new_question(self):
        response = QuestionServices.createNewQuestion(new_question)
        assert response["status"] == 201
        assert response["message"] == 'Pregunta creada satisfactoriamente'
        logging.debug(str(UserTransactions.getUserActivities(new_question["facebookId"])))
        assert len(UserTransactions.getUserActivities(new_question["facebookId"])["activities"]) != 0

    def test_update_question_answer(self):
        response = QuestionServices.updateQuestion(new_answer)
        assert response["status"] == 200
        assert response["message"] == 'Pregunta actualizada satisfactoriamente'
        logging.debug(str(UserTransactions.getUserActivities(new_answer["facebookId"])))
        assert len(UserTransactions.getUserActivities(new_answer["facebookId"])["activities"]) != 0

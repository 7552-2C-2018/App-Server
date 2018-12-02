from flask_restplus import Resource, Api, Namespace, reqparse, inputs

from server.services.Monitoring.monitor import monitor
from server.services.Validator.validateAuth import validateAuth
from server.Structures.Response import responses
from server.services.questionServices import QuestionServices
import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG)


api = Namespace('questions', description='Melli question-related endpoints')

path = 'questions/'

common_args = reqparse.RequestParser()
common_args.add_argument('facebookId', type=str, help='facebookId', location='headers', required=True)
common_args.add_argument('token', type=str, help='Token de acceso', location='headers', required=True)

new_question = common_args.copy()
new_question.add_argument('postId', type=str, help='id del post por el que se esta preguntandp', location='form', required=True)
new_question.add_argument('question', type=str, help='pregunta del post', location='form', required=True)

answer = common_args.copy()
answer.add_argument('respuesta', type=str, help='respuesta a la pregunta', location='form', required=True)


@api.route('/')
class Questions(Resource):

    @api.doc(responses=responses)
    @api.expect(new_question)
    @validateAuth
    def post(self):
        """Endpoint for creating a single question"""
        monitor(path, "post")
        args = new_question.parse_args()
        return_data = QuestionServices.createNewQuestion(args)
        return return_data["data"], return_data["status"], {'message': return_data["message"]}

@api.route('/postId=<string:postId>/')
class Answers(Resource):
    @api.doc(responses=responses)
    @api.expect(common_args)
    @validateAuth
    def get(self, postId):
        """Endpoint that gets all questions"""
        monitor(path, "get")
        return_data = QuestionServices.getAllQuestions(postId)
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/<string:questionId>/respuesta/')
class Answers(Resource):

    @api.doc(responses=responses)
    @api.expect(answer)
    @validateAuth
    def put(self, questionId):
        """Endpoint that update a single answer"""
        monitor(path + "questionId/respuesta/", "put")
        args = answer.parse_args()
        args['questionId'] = questionId
        return_data = QuestionServices.updateQuestion(args)
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/<string:questionId>')
class QuestionsAndAnswers(Resource):

    @api.doc(responses=responses)
    @api.expect(common_args)
    @validateAuth
    def get(self, questionId):
        """Endpoint that gets a single questions"""
        monitor(path + "questionId", "get")
        args = {}
        args['questionId'] = questionId
        return_data = QuestionServices.getQuestion(args)
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


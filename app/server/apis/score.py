import logging
import time

from flask_restplus import Resource, Namespace, reqparse

from server.Structures.Response import responses
from server.services.Monitoring.monitor import monitor
from server.services.Validator.validateAuth import validateAuth
from server.services.scoreServices import ScoreServices

logging.basicConfig(filename='debug.log', level=logging.DEBUG)


api = Namespace('score', description='Melli score-related endpoints')

path = 'score/'

common_args = reqparse.RequestParser()
common_args.add_argument('facebookId', type=str, help='facebookId', location='headers', required=True)
common_args.add_argument('token', type=str, help='Token de acceso', location='headers', required=True)

update_score = common_args.copy()
update_score.add_argument('value', type=float, help='Valor de la calificacion', location='form', required=True)
update_score.add_argument('comment', type=str, help='commentario sobre la calificacion', location='form')

new_score = update_score.copy()
new_score.add_argument('rol', type=str, help='Comprador o Vendedor', location='form', required=True)
new_score.add_argument('buyId', type=str, help='id de la compra por la que se esta calificando'
                                        , location='headers', required=True)


@api.route('/')
class Score(Resource):

    @api.doc(responses=responses)
    @api.expect(new_score)
    @validateAuth
    def post(self):
        """Endpoint for creating a single score"""
        time_start = time.time()
        return_data = ScoreServices.createNewScore(new_score.parse_args())
        time_end = time.time()
        monitor(time_start, time_end, path, "post")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/scorerUser')
class ScoreByScorerId(Resource):
    @api.doc(responses=responses)
    @api.expect(common_args)
    @validateAuth
    def get(self):
        """Endpoint that gets all scores from the user as scorer"""
        time_start = time.time()
        args = common_args.parse_args()
        return_data = ScoreServices.getScoreByScorerId(args)
        time_end = time.time()
        monitor(time_start, time_end, path, "get")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/scoredUser')
class ScoreByScoredId(Resource):
    @api.doc(responses=responses)
    @api.expect(common_args)
    @validateAuth
    def get(self):
        """Endpoint that gets all scores from the scored user"""
        time_start = time.time()
        args = common_args.parse_args()
        return_data = ScoreServices.getScoreByScoredId(args)
        time_end = time.time()
        monitor(time_start, time_end, path, "get")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/<string:buy_id>')
@api.param('buy_id', 'Id form buy')
class ScoreUpdate(Resource):
    @api.doc(responses=responses)
    @api.expect(update_score)
    @validateAuth
    def put(self, buy_id):
        """Endpoint that gets a single score"""
        time_start = time.time()
        args = update_score.parse_args()
        args['buyId'] = buy_id
        return_data = ScoreServices.updateScore(args)
        time_end = time.time()
        monitor(time_start, time_end, path, "get")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}

    @api.doc(responses=responses)
    @api.expect(common_args)
    @validateAuth
    def get(self, buy_id):
        """Endpoint that gets a score"""
        time_start = time.time()
        args = common_args.parse_args()
        args['buyId'] = buy_id
        return_data = ScoreServices.getScore(args)
        time_end = time.time()
        monitor(time_start, time_end, path, "get")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}

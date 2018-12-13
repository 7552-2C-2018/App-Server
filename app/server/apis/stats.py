import sys
from server.Structures.Response import responses, Responses
from server.services.Validator.validateAuth import validateAuth
import pytz
from bson.codec_options import CodecOptions
from flask_restplus import Resource, Namespace, reqparse
from server.setup import app
with app.app_context():
    monitor_collection = app.database.stats

api = Namespace('stats', description='Melli stats-related endpoints')


@api.route('/')
class Stats(Resource):
    @api.doc(responses=responses)
    def get(self):
        """Endpoint for checking requests stats"""
        try:
            pipeline = [
                {
                    '$group':
                    {
                        '_id': {'route': '$route', 'method': '$method', 'day': '$day', 'hour': '$hour'},
                        'totalRequests': {'$sum': 1},
                        'averageTimeElapsed': {'$avg': '$time_elapsed_ms'}
                    },
                    '$sort': {
                        'date_time': 1}
                }
            ]

            aware_colection = monitor_collection.with_options(
                codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('America/Argentina/Buenos_Aires')))
            cursor = aware_colection.aggregate(pipeline)
            data = {}
            for row in cursor:
                request_string = row['_id']['method'] + ": " + row['_id']['route']
                if request_string not in data:
                    data[request_string] = []

                data[request_string].append({
                    'daytime': str(row['_id']['day']) + ' - ' + str(row['_id']['hour']) + ' hs',
                    'avg_time_elapsed': row['averageTimeElapsed'],
                    'totalRequests': row['totalRequests']
                })
            return_data = Responses.success('Stats obtenidos satisfactoriamente', data)
            return return_data["data"], return_data["status"], {'message': return_data["message"]}
        except Exception:
            return_data = Responses.internalServerError('Error al obtener los stats')
            return return_data["data"], return_data["status"], {'message': return_data["message"]}

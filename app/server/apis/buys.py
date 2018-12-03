import time

from flask_restplus import Resource, Api, Namespace, reqparse, inputs

from server.services.Monitoring.monitor import monitor
from server.services.Validator.validateAuth import validateAuth, validateAuthServer
from server.services.buyServices import BuyServices
from server.Structures.Response import responses
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


api = Namespace('buys', description='Melli buy-related endpoints')

path = 'buys/'

common_args = reqparse.RequestParser()
common_args.add_argument('facebookId', type=str, help='facebookId', location='headers', required=True)
common_args.add_argument('token', type=str, help='Token de acceso', location='headers', required=True)

new_buy_args = common_args.copy()
new_buy_args.add_argument('postId', type=str, help='Id del post del producto a comprar',
                          location='headers', required=True)
new_buy_args.add_argument('price', type=str, help='Precio de la compra', location='form', required=True)

new_buy_args.add_argument('cardNumber', type=str, help='Numero de la tarjeta utilizada para la compra', location='form')
new_buy_args.add_argument('cardDate', type=str, help='ExpDate de la tarjeta utilizada para la compra', location='form')
new_buy_args.add_argument('cardName', type=str,
                          help='Nombre del titular de la tarjeta utilizada para la compra', location='form')
new_buy_args.add_argument('cardBank', type=str,
                          help='Nombre del banco de la tarjeta utilizada para la compra', location='form')
new_buy_args.add_argument('cardCVV', type=str, help='Cvv de la tarjeta utilizada para la compra', location='form')

new_buy_args.add_argument('street', type=str, help='Calle de shipping', location='form')
new_buy_args.add_argument('cp', type=str, help='Codigo postal de shipping', location='form')
new_buy_args.add_argument('floor', type=str, help='Piso del shipping', location='form')
new_buy_args.add_argument('dept', type=str, help='Depto del shipping', location='form')
new_buy_args.add_argument('city', type=str, help='Ciudad del shipping', location='form')

modify_state = common_args.copy()
modify_state.add_argument('State', type=str, help='Id del post del producto a comprar',
                          location='form', required=True)

server_communication_args = reqparse.RequestParser()
server_communication_args.add_argument('UserId', type=str, help='Id del servidor', location='headers', required=True)
server_communication_args.add_argument('Token', type=str, help='Token de acceso', location='headers', required=True)


@api.route('/')
class Buys(Resource):
    @api.doc(responses=responses)
    @api.expect(new_buy_args)
    @validateAuth
    def post(self):
        """Endpoint for creating a single buy"""
        time_start = time.time()
        return_data = BuyServices.createNewBuy(new_buy_args.parse_args())
        time_end = time.time()
        monitor(time_start, time_end, path, "post")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/<string:buy_id>')
@api.param('buy_id', 'Id form buy')
class Buy(Resource):
    @api.doc(responses=responses)
    @api.expect(common_args)
    @validateAuth
    def get(self, buy_id):
        """Endpoint that gets a single buy"""
        time_start = time.time()
        args = common_args.parse_args()
        args['buyId'] = buy_id
        return_data = BuyServices.getBuy(args)
        time_end = time.time()
        monitor(time_start, time_end, path, "get")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}

    @api.doc(responses=responses)
    @api.expect(modify_state)
    @validateAuth
    def put(self, buy_id):
        """Endpoint that modify a single buy"""
        time_start = time.time()
        args = modify_state.parse_args()
        args['buyId'] = buy_id
        return_data = BuyServices.updateBuy(args)
        time_end = time.time()
        monitor(time_start, time_end, path, "put")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/user=<string:user_id>')
@api.param('user_id', 'Id from buyer')
class BuyByUser(Resource):
    @api.doc(responses=responses)
    @api.expect(common_args)
    @validateAuth
    def get(self, user_id):
        """Endpoint that gets a all buys from user"""
        time_start = time.time()
        args = common_args.parse_args()
        args['userId'] = user_id
        return_data = BuyServices.getBuysByUser(args)
        time_end = time.time()
        monitor(time_start, time_end, path, "get")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/seller=<string:seller_id>')
@api.param('seller_id', 'Id from seller')
class BuyBySeller(Resource):
    @api.doc(responses=responses)
    @api.expect(common_args)
    @validateAuth
    def get(self, seller_id):
        """Endpoint that gets a all buys from seller"""
        time_start = time.time()
        args = common_args.parse_args()
        args['seller_id'] = seller_id
        return_data = BuyServices.getBuysBySeller(args)
        time_end = time.time()
        monitor(time_start, time_end, path, "get")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/trackingId=<string:tracking_id>')
@api.param('trackingId', 'Id from trackingId')
class BuyByTracking(Resource):
    @api.doc(responses=responses)
    @api.expect(server_communication_args)
    @validateAuthServer
    def put(self, tracking_id):
        """Endpoint that updates buy state by paymentId"""
        time_start = time.time()
        args = common_args.parse_args()
        args['tracking_id'] = tracking_id
        return_data = BuyServices.update_buy_by_payment_id(args)
        time_end = time.time()
        monitor(time_start, time_end, path, "get")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/paymentId=<string:payment_id>')
@api.param('paymentId', 'Id from payment_id')
class BuyByShipment(Resource):
    @api.doc(responses=responses)
    @api.expect(server_communication_args)
    @validateAuthServer
    def put(self, payment_id):
        """Endpoint that updates buy state by shipmentId"""
        time_start = time.time()
        args = common_args.parse_args()
        args['payment_id'] = payment_id
        return_data = BuyServices.update_buy_by_payment_id(args)
        time_end = time.time()
        monitor(time_start, time_end, path, "get")
        return return_data["data"], return_data["status"], {'message': return_data["message"]}

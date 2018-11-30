from flask_restplus import Resource, Api, Namespace, reqparse, inputs
from server.services.Validator.validateAuth import validateAuth
from server.services.buyServices import BuyServices
from server.Structures.Response import responses
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


api = Namespace('buys', description='Melli buy-related endpoints')

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


@api.route('/')
class Buys(Resource):
    @api.doc(responses=responses)
    @api.expect(new_buy_args)
    @validateAuth
    def post(self):
        """Endpoint for creating a single buy"""
        return_data = BuyServices.createNewBuy(new_buy_args.parse_args())
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/<string:buy_id>')
@api.param('buy_id', 'Id form buy')
class Buy(Resource):
    @api.doc(responses=responses)
    @api.expect(common_args)
    @validateAuth
    def get(self, buy_id):
        """Endpoint that gets a single buy"""
        args = common_args.parse_args()
        args['buyId'] = buy_id
        return_data = BuyServices.getBuy(args)
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/user=<string:user_id>')
@api.param('user_id', 'Id from buyer')
class BuyByUser(Resource):
    @api.doc(responses=responses)
    @api.expect(common_args)
    @validateAuth
    def get(self, user_id):
        """Endpoint that gets a all buys from user"""
        args = common_args.parse_args()
        args['userId'] = user_id
        return_data = BuyServices.getBuysByUser(args)
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/seller=<string:seller_id>')
@api.param('seller_id', 'Id from seller')
class BuyBySeller(Resource):
    @api.doc(responses=responses)
    @api.expect(common_args)
    @validateAuth
    def get(self, seller_id):
        """Endpoint that gets a all buys from seller"""
        args = common_args.parse_args()
        args['seller_id'] = seller_id
        return_data = BuyServices.getBuysBySeller(args)
        return return_data["data"], return_data["status"], {'message': return_data["message"]}
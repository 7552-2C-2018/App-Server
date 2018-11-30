from flask_restplus import Resource, Api, Namespace, reqparse, inputs
from server.services.Validator.validateAuth import validateAuth
from server.services.postServices import PostServices
from server.Structures.Response import responses
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


api = Namespace('posts', description='Melli post-related endpoints')

common_args = reqparse.RequestParser()
common_args.add_argument('facebookId', type=str, help='facebookId', location='headers', required=True)
common_args.add_argument('token', type=str, help='Token de acceso', location='headers', required=True)

get_post_filter_args = common_args.copy()
get_post_filter_args.add_argument('distancia', type=int, help='radio de la circunferencia del filtro por distancia',
                                  location='headers')
get_post_filter_args.add_argument('latitud', type=float,
                                  help='latitud del centro de la circunferencia del filtro por distancia',
                                  location='headers')
get_post_filter_args.add_argument('longitud', type=float,
                                  help='latitud del centro de la circunferencia del filtro por distancia',
                                  location='headers')
get_post_filter_args.add_argument('precioMaximo',
                                  type=int, help='precio maximo del producto filtrado', location='headers')
get_post_filter_args.add_argument('precioMinimo',
                                  type=int, help='precio minimo del producto filtrado', location='headers')
get_post_filter_args.add_argument('estado',
                                  type=str, help='estado del producto del post'
                                                  ' (nuevo, usado, ninguno para ambos)',
                                  location='headers')
get_post_filter_args.add_argument('envio', type=bool,
                                  help='filtro por productos por los cuales se realizan envios', location='headers')

new_post_args = common_args.copy()
new_post_args.add_argument('title', type=str, help='titulo del post', location='form', required=True)
new_post_args.add_argument('desc', type=str, help='descripcion del post', location='form', required=True)
new_post_args.add_argument('stock', type=int, help='stock del post', location='form', required=True)
new_post_args.add_argument('payments', type=str, help='tipos de pago', location='form', required=True,action='split')
new_post_args.add_argument("price",  type=int, help='precio del producto', location='form', required=True)
new_post_args.add_argument("new", type=inputs.boolean,
                           help='flag si el producto es nuevo o usado', location='form', required=True)
new_post_args.add_argument("category", type=str, help='categoria del producto', location='form', required=True)
new_post_args.add_argument("pictures", type=str, help='imagenes del producto', location='form',action='split')
new_post_args.add_argument("shipping", type=inputs.boolean,
                              help='si el producto puede o no ser enviado por via maritima',
                              location='form',required=True)
new_post_args.add_argument("latitude", type=float, help='latitud', location='form', required=True)
new_post_args.add_argument("longitude", type=float, help='longitud', location='form', required=True)

update_post_args = common_args.copy()
update_post_args.add_argument('estado', type=str, help='nuevo estado del post', location='form', required=True)
"""
update_post_args.add_argument('title', type=str, help='titulo del post', location='form')
update_post_args.add_argument('desc', type=str, help='descripcion del post', location='form')
update_post_args.add_argument('stock', type=int, help='stock del post', location='form')
update_post_args.add_argument('payments', type=str, help='tipos de pago', location='form',action='split')
update_post_args.add_argument("price",  type=int, help='precio del producto', location='form')
update_post_args.add_argument("new", type=inputs.boolean, help='si el producto es nuevo o usado', location='form')
update_post_args.add_argument("category", type=str, help='categoria del producto', location='form')
update_post_args.add_argument("pictures", type=str, help='imagenes del producto', location='form',action='split')
update_post_args.add_argument("shipping", type=inputs.boolean,
                              help='si el producto puede o no ser enviado por via maritima', location='form')
update_post_args.add_argument("latitude", type=float, help='latitud', location='form')
update_post_args.add_argument("longitude", type=float, help='longitud', location='form')
"""


@api.route('/')
class Posts(Resource):
    @api.doc(responses=responses)
    @api.expect(get_post_filter_args)
    @validateAuth
    def get(self):
        """Endpoint that gets all posts"""
        args = get_post_filter_args.parse_args()
        return_data = PostServices.getAllPosts(args)
        return return_data["data"], return_data["status"], {'message': return_data["message"]}

    @api.doc(responses=responses)
    @api.expect(new_post_args)
    @validateAuth
    def post(self):
        """Endpoint for creating a single post"""
        return_data = PostServices.createNewPost(new_post_args.parse_args())
        return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/<string:post_id>')
class Post(Resource):
    @api.doc(responses=responses)
    @api.expect(common_args)
    @validateAuth
    def get(self, post_id):
        """Endpoint that gets a single post"""
        args = common_args.parse_args()
        args['postId'] = post_id
        logging.debug("post: " + str(args))
        return_data = PostServices.getPost(args)
        return return_data["data"], return_data["status"], {'message': return_data["message"]}

    @api.doc(responses=responses)
    @api.expect(update_post_args)
    @validateAuth
    def put(self, post_id):
        """Endpoint for updating a single post"""
        args = update_post_args.parse_args()
        args['postId'] = post_id
        return_data = PostServices.updatePost(args)
        return return_data["data"], return_data["status"], {'message': return_data["message"]}

@api.route('/user=<string:user_id>')
class PostByUser(Resource):
    @api.doc(responses=responses)
    @api.expect(common_args)
    @validateAuth
    def get(self, user_id):
        """Endpoint that gets a all posts from user"""
        args = common_args.parse_args()
        args['userId'] = user_id
        logging.debug("post: " + str(args))
        return_data = PostServices.getPostByUser(args)
        return return_data["data"], return_data["status"], {'message': return_data["message"]}
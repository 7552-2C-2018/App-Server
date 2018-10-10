from flask_restplus import Resource,Api, Namespace, reqparse
from server.services.Validator.validateAuth import validateAuth
from server.services.postServices import PostServices
from server.Structures.Response import responses

api = Namespace('posts', description='Melli post-related endpoints')

common_args = reqparse.RequestParser()
common_args.add_argument('facebookId', type=str, help='facebookId', location='headers')
common_args.add_argument('access-token', type=str, help='Token de acceso', location='headers')

get_post = common_args.copy()
get_post.add_argument('post_id', type=str, help='Id del post a obtener', location='args')

new_post_args = common_args.copy()
new_post_args.add_argument('title', type=str, help='titulo del post', location='form', required=True)
new_post_args.add_argument('desc', type=str, help='descripcion del post', location='form', required=True)
new_post_args.add_argument('stock', type=int, help='stock del post', location='form', required=True)
new_post_args.add_argument('payments', type=list, help='tipos de pago', location='form', required=True)
new_post_args.add_argument('email', type=str, help='mail', location='form', required=True)

update_post_args = common_args.copy()
update_post_args.add_argument('title', type=str, help='titulo del post', location='form')
update_post_args.add_argument('desc', type=str, help='descripcion del post', location='form')
update_post_args.add_argument('stock', type=int, help='stock del post', location='form')
update_post_args.add_argument('payments', type=list, help='tipos de pago', location='form')
update_post_args.add_argument('email', type=str, help='mail', location='form')

login = reqparse.RequestParser()
login.add_argument('facebookId', type=str, help='facebookId', location='headers', required=True)
login.add_argument('token', type=str, help='token fb', location='headers', required=True)

register = login.copy()
register.add_argument('firstName', type=str, help='nombre', location='form', required=True)
register.add_argument('lastName', type=str, help='apellido', location='form', required=True)
register.add_argument('photoUrl', type=str, help='foto', location='form', required=True)
register.add_argument('email', type=str, help='mail', location='form', required=True)

@api.route('/')
@api.doc(responses=responses)
class Post(Resource):

	@api.expect(get_post)
	@validateAuth
	def get(self):
		return_data = PostServices.getPost(get_post.parse_args())
		return return_data["data"], return_data["status"], {'message': return_data["message"]}

	@api.expect(new_post_args)
	@validateAuth
	def post(self):
		return_data = PostServices.createNewPost(new_post_args.parse_args())
		return return_data["data"], return_data["status"], {'message': return_data["message"]}

	@api.expect(update_post_args)
	@validateAuth
	def put(self):
		return_data = PostServices.updatePost(update_post_args.parse_args())
		return return_data["data"], return_data["status"], {'message': return_data["message"]}


@api.route('/get_all')
class Posts(Resource):

	@api.expect(common_args)
	@validateAuth
	def get(self):
		return_data = PostServices.getAllPosts(common_args.parse_args())
		return return_data["data"], return_data["status"], {'message': return_data["message"]}
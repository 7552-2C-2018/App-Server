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


@api.doc(responses=responses)
class Post(Resource):
	@api.route('/all')
	@api.expect(common_args)
	@validateAuth
	def get(self):
		return_data = PostServices.getAllPosts(common_args.parse_args())
		return {'message': return_data["message"]}, return_data["status"], {'body': return_data["data"]}

	@api.route('/')
	@api.expect(get_post)
	@validateAuth
	def get(self):
		return_data = PostServices.getPost(get_post.parse_args())
		return {'message': return_data["message"]}, return_data["status"], {'body': return_data["data"]}

	@api.route('/')
	@api.expect(new_post_args)
	@validateAuth
	def post(self):
		return PostServices.createNewPost(new_post_args.parse_args())

	@api.route('/')
	@api.expect(update_post_args)
	@validateAuth
	def put(self):
		return PostServices.updatePost(update_post_args.parse_args())


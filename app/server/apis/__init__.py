from flask_restplus import Api
from .users import api as users
from .products import api as products
from .posts import api as posts
from .buys import api as buys
from .questions import api as questions
from .stats import api as stats
from .ping import api as ping

api = Api(version='0.1', title='Melli App API', description='Api del servidor de Melli App',)


def registerApi(app):

    api.namespaces.clear()

    api.add_namespace(users)
    api.add_namespace(products)
    api.add_namespace(posts)
    api.add_namespace(buys)
    api.add_namespace(questions)
    api.add_namespace(ping)
    api.add_namespace(stats)
    api.init_app(app)

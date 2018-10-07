from flask_restplus import Api
from .users import api as users
from .products import api as products
from .ping import api as ping

api = Api(version='0.1', title='Melli App API', description='Api del servidor de Melli App',)


def registerApi(app):

    api.namespaces.clear()

    api.add_namespace(users)
    api.add_namespace(products)
    api.add_namespace(ping)
    api.init_app(app)
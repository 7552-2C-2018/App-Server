from flask_restplus import Api

from .score import api as score
from .users import api as users
from .resources import api as resources
from .posts import api as posts
from .buys import api as buys
from .questions import api as questions
from .stats import api as stats
from .estimation import api as estimation
from .ping import api as ping

api = Api(version='1', title='Melli App API', description='Api del servidor de Melli App',)


def registerApi(app):

    api.namespaces.clear()

    api.add_namespace(users)
    api.add_namespace(resources)
    api.add_namespace(posts)
    api.add_namespace(buys)
    api.add_namespace(questions)
    api.add_namespace(ping)
    api.add_namespace(stats)
    api.add_namespace(estimation)
    api.add_namespace(score)
    api.init_app(app)

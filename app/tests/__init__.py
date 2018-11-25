import os

os.environ.setdefault('MONGO_URL', 'mongodb://mongo-db:27017/testDatabase')
import unittest
from server.setup import app


class GenericTest(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        try:
            app.database.users.drop()
        except Exception:
            pass
        app.database.create_collection('users')
        try:
            app.database.posts.drop()
        except Exception:
            pass
        app.database.create_collection('posts')
        app.database.users.insert_one({"facebookId": "102510700706099",
                                       "firstName": "mark",
                                       "lastName": "zuc",
                                       "photoUrl": "foto",
                                       "email": "mail"})
        app.database.posts.insert_one({
            "_id": {
                "facebookId": "102510700706087",
                "publication_date": 1539228792
            },
            "ID": "1025107007060871539228792",
            "category": "test",
            "coordenates": [
                12,
                13
            ],
            "description": "Desde swagger",
            "new": True,
            "payments": [
                "EFECTIVO"
            ],
            "pictures": None,
            "price": 10,
            "shipping": False,
            "stock": 2,
            "title": "Prueba"
        })


def tearDown(self):
    self.app_context.pop()

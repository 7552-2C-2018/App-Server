import os
MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    os.environ.setdefault('MONGO_URL', 'mongodb://mongo-db:27017/testDatabase')
    MONGO_URL
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
        try:
            app.database.posts.drop()
        except Exception:
            pass
        try:
            app.database.buys.drop()
        except Exception:
            pass
        try:
            app.database.buy_states.drop()
        except Exception:
            pass
        app.database.create_collection('users')
        app.database.create_collection('posts')
        app.database.create_collection('buy_states')
        app.database.create_collection('buys')
        self.setUpDbEnviroment()


    def setUpDbEnviroment(self):
        app.database.users.insert_one({"facebookId": "102510700706099",
                                       "firstName": "mark",
                                       "lastName": "zuc",
                                       "photoUrl": "foto",
                                       "email": "mail"})
        app.database.users.insert_one({"facebookId": "99",
                                       "firstName": "test",
                                       "lastName": "user",
                                       "photoUrl": "foto",
                                       "email": "mail@Comprame.com"})
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
        app.database.buys.insert_one({
            "_id": {
                "facebookId": "99",
                "publication_date": 1539228792
            },
            "ID": "991539228792",
            "postId": "1025107007060871539228792",
            "street": "calle falsa 123",
            "price": 100,
            "paymentMethod": "Efectivo"
            })
        app.database.buys.insert_one({
            "_id": {
                "facebookId": "99",
                "publication_date": 1539228999
            },
            "ID": "991539228999",
            "postId": "1025107007060871539228792",
            "street": "calle falsa 123",
            "price": 100,
            "paymentMethod": "Credito",
            "payment": 1,
            "tracking": 1
        })
        app.database.buy_states.insert({"_id":1, "state": "Comprado"})
        app.database.buy_states.insert({"_id":2, "state": "Finalizado"})
        app.database.buy_states.insert({"_id":3, "state": "Calificado"})
        app.database.buy_states.insert({"_id":4, "state": "Completado"})
        app.database.buy_states.insert({"_id":6, "state": "Pago Pendiente", "payment": True})
        app.database.buy_states.insert({"_id":7, "state": "Pago rechazado", "payment": True})
        app.database.buy_states.insert({"_id":8, "state": "Pago aceptado", "payment": True})
        app.database.buy_states.insert({"_id":9, "state": "Envio en progreso", "tracking": True})
        app.database.buy_states.insert({"_id":10, "state": "Pendiente de envio", "tracking": True})
        app.database.buy_states.insert({"_id":11, "state": "Envio realizado", "tracking": True})


def tearDown(self):
    self.app_context.pop()

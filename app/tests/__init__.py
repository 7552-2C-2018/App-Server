import os
MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    os.environ.setdefault('MONGO_URL', 'mongodb://127.0.0.1:27017/testDatabase')
    MONGO_URL = os.environ.get('MONGO_URL')
import unittest
from server.setup import app


class GenericTest(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        self.flush_database()
        app.database.create_collection('users')
        app.database.create_collection('posts')
        app.database.create_collection('buy_states')
        app.database.create_collection('buys')
        app.database.create_collection('questions')
        app.database.create_collection('scores')
        self.setUpDbEnviroment()


    def setUpDbEnviroment(self):
        app.database.users.insert_one({"facebookId": "102510700706099",
                                       "firstName": "mark",
                                       "lastName": "zuc",
                                       "photoUrl": "foto",
                                       "email": "mail"})
        app.database.users.insert_one({"facebookId": "102510700706087",
                                       "firstName": "test",
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
            "estado": "Comprado",
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
            "estado": "Comprado",
            "price": 100,
            "paymentMethod": "Credito",
            "payment": 1,
            "tracking": 1
        })
        app.database.questions.insert_one({
            "_id": {
                "postId": "1025107007060871539228792",
                "publication_date": 1999439
            },
            "ID": "10251070070608715392287921999439",
            "pregunta": "cuanto me cobras por 1000?",
            "answer": "lo mismo capo",
            "answer_date": 19994399,
            "userId": "99"
        })
        app.database.scores.insert_one({
            "_id": {
                "scorerUserId": "99",
                "buy_id": "991539228792"
            },
            "scoredUserId": "102510700706087",
            "comment": "muy amable como vendedor",
            "value": 4
        })
        app.database.scores.insert_one({
            "_id": {
                "scorerUserId": "102510700706087",
                "buy_id": "991539228792"
            },
            "scoredUserId": "99",
            "comment": "muy amable como comprador",
            "value": 4
        })
        app.database.buy_states.insert({"_id": 1, "estado": "Comprado"})
        app.database.buy_states.insert({"_id": 2, "estado": "Finalizado"})
        app.database.buy_states.insert({"_id": 3, "estado": "Calificado"})
        app.database.buy_states.insert({"_id": 4, "estado": "Completado"})
        app.database.buy_states.insert({"_id": 6, "estado": "Pago Pendiente", "payment": True})
        app.database.buy_states.insert({"_id": 7, "estado": "Pago rechazado", "payment": True})
        app.database.buy_states.insert({"_id": 8, "estado": "Pago aceptado", "payment": True})
        app.database.buy_states.insert({"_id": 9, "estado": "Envio en progreso", "tracking": True})
        app.database.buy_states.insert({"_id": 10, "estado": "Pendiente de envio", "tracking": True})
        app.database.buy_states.insert({"_id": 11, "estado": "Envio realizado", "tracking": True})

    def flush_database(self):
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
        try:
            app.database.questions.drop()
        except Exception:
            pass
        try:
            app.database.scores.drop()
        except Exception:
            pass

def tearDown(self):
    self.app_context.pop()

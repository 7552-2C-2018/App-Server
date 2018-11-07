from server.setup import app
import logging
import json
import datetime
import time
from bson import json_util, ObjectId
logging.basicConfig(filename='debug.log', level=logging.DEBUG)
with app.app_context():
    buysCollection = app.database.buys


class BuyTransactions:

    def __init__(self):
        pass

    @staticmethod
    def __validate_estado(estado):
        return estado in ["Comprado", "Pagado", "Recibido", "Calificado"]

    @staticmethod
    def findBuyBySellerId(seller_id):
        pipeline = [
            {
                u"$project": {
                    u"_id": 0,
                    u"a": u"$$ROOT"
                }
            },
            {
                u"$lookup": {
                    u"localField": u"a.postId",
                    u"from": u"posts",
                    u"foreignField": u"ID",
                    u"as": u"b"
                }
            },
            {
                u"$unwind": {
                    u"path": u"$b",
                    u"preserveNullAndEmptyArrays": False
                }
            },
            {
                u"$match": {
                    u"b.facebookID": seller_id
                }
            },
            {
                u"$project": {
                    u"ID": u"$a.ID",
                    u"title": u"$b.title",
                    u"pictures": u"$b.pictures",
                    u"estado": u"$a.estado"
                }
            },
        ]

        cursor = buysCollection.aggregate(
            pipeline,
            allowDiskUse=True
        )
        return list(cursor)

    @staticmethod
    def findBuyById(buy_id):
        pipeline = [
            {
                u"$project": {
                    u"_id": 0,
                    u"a": u"$$ROOT"
                }
            },
            {
                u"$lookup": {
                    u"localField": u"a.postId",
                    u"from": u"posts",
                    u"foreignField": u"ID",
                    u"as": u"b"
                }
            },
            {
                u"$unwind": {
                    u"path": u"$b",
                    u"preserveNullAndEmptyArrays": False
                }
            },
            {
                u"$match": {
                    u"a.ID": buy_id
                }
            },
            {
                u"$project": {
                    u"ID": u"$a.ID",
                    u"title": u"$b.title",
                    u"pictures": u"$b.pictures",
                    u"estado": u"$a.estado"
                }
            },
        ]

        cursor = buysCollection.aggregate(
            pipeline,
            allowDiskUse=True
        )
        return list(cursor)[0]

    @staticmethod
    def newBuy(data):
        buy_date = time.mktime(datetime.datetime.utcnow().timetuple())
        buy_id = data['facebookId'] + str(buy_date)
        data["ID"] = buy_id
        data["estado"] = "Comprado"
        data.pop("token")
        buysCollection.insert_one({"_id": {"facebookId": data['facebookId'], "buy_date": buy_date}})
        buysCollection.update_one({"_id": {"facebookId": data['facebookId'], "buy_date": buy_date}},
                                     {'$set': data})
        return buy_id

    @staticmethod
    def findBuyByUserId(user_id):
        pipeline = [
            {
                u"$project": {
                    u"_id": 0,
                    u"a": u"$$ROOT"
                }
            },
            {
                u"$lookup": {
                    u"localField": u"a.post_id",
                    u"from": u"posts",
                    u"foreignField": u"ID",
                    u"as": u"b"
                }
            },
            {
                u"$unwind": {
                    u"path": u"$b",
                    u"preserveNullAndEmptyArrays": False
                }
            },
            {
                u"$match": {
                    u"a._id.facebookId": user_id
                }
            },
            {
                u"$project": {
                    u"a.ID": u"$a.ID",
                    u"b.title": u"$b.title",
                    u"b.pictures": u"$b.pictures",
                    u"a.estado": u"$a.estado"
                }
            },
        ]

        cursor = buysCollection.aggregate(
            pipeline,
            allowDiskUse=True
        )
        return list(cursor)

    @staticmethod
    def updateBuyData(data):
        estado_valido = PostTransactions.__validate_estado(data["estado"])
        if estado_valido:
            return buysCollection.update_one({'ID': data['buyId']}, {'$set': {"estado": data["estado"]}})
        else:
            return "estado Invalido"

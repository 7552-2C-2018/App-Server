from server.setup import app
import logging
import json
import datetime
import time
from server.Communication.SharedServerCommunication.sharedServerRequests import SharedServerRequests


logging.basicConfig(filename='debug.log', level=logging.DEBUG)
with app.app_context():
    buysCollection = app.database.buys


class BuyTransactions:

    def __init__(self):
        pass

    @staticmethod
    def __parseData(data):
        parsed_data = {}
        if data["postId"] is not None:
            parsed_data["postId"] = data["postId"]
        if data["cardNumber"] is not None:
            payment_response = SharedServerRequests.newPayment(data)

            if payment_response is None:
                logging.debug("se rompio le payment")
                raise Exception
            logging.debug("payment: " + str(payment_response))
            parsed_data["payment"] = payment_response["id"]

        if data["street"] is not None:

            tracking_response = SharedServerRequests.newTracking(data)
            if tracking_response is None:
                logging.debug("se rompio la street")
                raise Exception
            parsed_data["shipping"] = tracking_response["id"]
            logging.debug("tracking: " + str(tracking_response))

        return parsed_data

    @staticmethod
    def __validate_estado(estado):
        return estado in ["Comprado", "Pagado", "Recibido", "Calificado"]

    @staticmethod
    def findBuyBySellerId(seller_id):
        pipeline = [
            {
                u"$project": {
                    u"_id": 1,
                    u"buys": u"$$ROOT"
                }
            },
            {
                u"$lookup": {
                    u"localField": u"buys.postId",
                    u"from": u"posts",
                    u"foreignField": u"ID",
                    u"as": u"posts"
                }
            },
            {
                u"$unwind": {
                    u"path": u"$posts",
                    u"preserveNullAndEmptyArrays": False
                }
            },
            {
                u"$match": {
                    u"posts._id.facebookId": seller_id
                }
            },
            {
                u"$project": {
                    u"ID": u"$buys.ID",
                    u"title": u"$posts.title",
                    u"picture": {u"$slice": ["$posts.pictures", 1]},
                    u"estado": u"$buys.estado"
                }
            }
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
        buy_id = data['facebookId'] + str(int(buy_date))
        data["ID"] = buy_id
        data["estado"] = "Comprado"
        parsed_data = BuyTransactions.__parseData(data)
        buysCollection.insert_one({"_id": {"facebookId": data['facebookId'], "buy_date": buy_date}})
        buysCollection.update_one({"_id": {"facebookId": data['facebookId'], "buy_date": buy_date}},
                                     {'$set': parsed_data})
        return buy_id

    @staticmethod
    def findBuyByUserId(user_id):
        pipeline = [
            {
                u"$project": {
                    u"_id": 1,
                    u"buys": u"$$ROOT"
                }
            },
            {
                u"$lookup": {
                    u"localField": u"buys.postId",
                    u"from": u"posts",
                    u"foreignField": u"ID",
                    u"as": u"posts"
                }
            },
            {
                u"$unwind": {
                    u"path": u"$posts",
                    u"preserveNullAndEmptyArrays": False
                }
            },
            {
                u"$match": {
                    u"buys._id.facebookId": user_id
                }
            },
            {
                u"$project": {
                    u"ID": u"$buys.ID",
                    u"title": u"$posts.title",
                    u"picture": {u"$slice": ["$posts.pictures", 1]},
                    u"estado": u"$buys.estado"
                }
            }
        ]
        cursor = buysCollection.aggregate(
            pipeline,
            allowDiskUse=True
        )
        return list(cursor)

    @staticmethod
    def updateBuyData(data):
        estado_valido = BuyTransactions.__validate_estado(data["estado"])
        if estado_valido:
            return buysCollection.update_one({'ID': data['buyId']}, {'$set': {"estado": data["estado"]}})
        else:
            return "estado Invalido"
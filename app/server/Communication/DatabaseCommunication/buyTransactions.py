from server.Communication.DatabaseCommunication.postTransactions import PostTransactions
from server.Communication.DatabaseCommunication.resourceTransactions import ResourceTransactions
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
        parsed_data["postId"] = data["postId"]
        parsed_data["paymentMethod"] = data["paymentMethod"]
        post_data = PostTransactions.find_post_by_post_id(data["postId"])
        if "cardNumber" in data.keys() and data["cardNumber"] is not None:
            payment_response = SharedServerRequests.newPayment(data, post_data)
            if payment_response is None:
                logging.debug("se rompio le payment")
                raise Exception
            logging.debug("payment: " + str(payment_response))
            parsed_data["payment"] = payment_response

        if "street" in data.keys() and data["street"] is not None:
            tracking_response = SharedServerRequests.newTracking(data, post_data)
            if tracking_response is None:
                logging.debug("se rompio la street")
                raise Exception
            parsed_data["shipping"] = tracking_response
            logging.debug("tracking: " + str(tracking_response))
        parsed_data["ID"] = data["ID"]
        parsed_data["estado"] = data["estado"]
        return parsed_data


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
                    u"postId": u"$buys.postId",
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
                    u"postId": u"$a.postId",
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
        try:
            return list(cursor)[0]
        except Exception:
            return None

    @staticmethod
    def findBuyerById(data):
        return buysCollection.find_one({"ID": data}, {"_id": 1, "postId": 1})

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
                u"$lookup": {
                    u"localField": u"buys.ID",
                    u"from": u"scores",
                    u"foreignField": u"_id.buy_id",
                    u"as": u"scores"
                }
            },
            {
                u"$unwind": {
                    u"path": u"$scores",
                    u"preserveNullAndEmptyArrays": True
                }
            },
            {
                u"$match": {
                    u"buys._id.facebookId": user_id,
                    u"scores._id.scorerUserId": {"$ne": user_id}
                }
            },
            {
                u"$project": {
                    u"ID": u"$buys.ID",
                    u"postId": u"$buys.postId",
                    u"title": u"$posts.title",
                    u"picture": {u"$slice": ["$posts.pictures", 1]},
                    u"estado": u"$buys.estado",
                    u"value": u"$scores.value"
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
        estado = BuyTransactions.__get_estado(data["estado"])
        logging.debug("estado:" + str(estado))
        if estado is not None or data["State"] == "Completado":
            has_tracking = buysCollection.find_one({'ID': data['buyId'], 'tracking': {"$exists": True}})
            tracking_state = BuyTransactions.__get_estado_tracking(data["estado"])
            if has_tracking is not None:
                if tracking_state is not None:
                    logging.debug("invalid by tracking")
                    raise Exception
            has_payment = buysCollection.find_one({'ID': data['buyId'], 'payment': {"$exists": True}})
            payment_state = BuyTransactions.__get_estado_payment(data["estado"])
            if has_payment is not None:
                if payment_state is not None:
                    logging.debug("invalid by payment")
                    raise Exception
            if data["estado"] == "Envio realizado":
                data["estado"] = "Finalizado"
            BuyTransactions.__sendNotifications(data)
            return buysCollection.update_one({'ID': data['buyId']}, {'$set': {"estado": estado}})
        else:
            raise Exception


    @staticmethod
    def update_buy_by_tracking_id(data):
        data["State"] = BuyTransactions.__get_estado_tracking(data["State"])
        if data["State"] is not None or data["State"] == "Completado":
            if data["State"] == "Envio realizado":
                data["State"] = "Finalizado"
            BuyTransactions.__sendNotifications(data)
            return buysCollection.update_one({'tracking_id': data['tracking_id']}, {'$set': {"estado": data["State"]}})
        else:
            return "Estado Invalido"

    @staticmethod
    def update_buy_by_payment_id(data):
        data["State"] = BuyTransactions.__get_estado_payment(data["State"])
        BuyTransactions.__sendNotifications(data)
        if data["State"] is not None and data["State"] != "Completado":
            return buysCollection.update_one({'payment_id': data['payment_id']}, {'$set': {"estado": data["State"]}})
        else:
            return "Estado Invalido"

    @staticmethod
    def __get_estado(estado):
        logging.debug("estado:" + str(estado))
        return ResourceTransactions.get_buy_states_by_id(estado)

    @staticmethod
    def __get_estado_tracking(estado):
        return ResourceTransactions.get_buy_tracking_states_by_id(estado)

    @staticmethod
    def __get_estado_payment( estado):
        return ResourceTransactions.get_buy_payment_states_by_id(estado)

    @staticmethod
    def __sendNotifications(data):
        pass

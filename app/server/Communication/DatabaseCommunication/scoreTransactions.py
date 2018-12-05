from server.Communication.DatabaseCommunication.buyTransactions import BuyTransactions
from server.Communication.DatabaseCommunication.postTransactions import PostTransactions
from server.Communication.DatabaseCommunication.userTransactions import UserTransactions
from server.setup import app
import logging
import json
import datetime
import time
from server.Communication.SharedServerCommunication.sharedServerRequests import SharedServerRequests


logging.basicConfig(filename='debug.log', level=logging.DEBUG)
with app.app_context():
    scoresCollection = app.database.scores

ESTADO_CALIFICADO = 3
ESTADO_COMPLETADO = 4

class ScoreTransactions:

    def __init__(self):
        pass

    @staticmethod
    def create_new_score(data):

        calificado = ScoreTransactions.__get_calificado(data)
        insert_data = data.copy()
        insert_data.pop("facebookId", None)
        insert_data.pop("token", None)
        if calificado == data['facebookId']:
            return None
        if insert_data["comment"] is None:
            insert_data["comment"] = ""
        try:
            scoresCollection.insert_one({"_id": {"scorerUserId": data['facebookId'],
                                                 "buy_id": data["buyId"]}})
            scoresCollection.update_one({"_id": {"scorerUserId": data['facebookId'],
                                                 "buy_id": data["buyId"]}},
                                        {'$set': {"scoredUserId": calificado,
                                                  "value": data['value'],
                                                  "comment": data['comment']}})
        except Exception:
            return "calificado"
        return calificado
    @staticmethod
    def update_score(data):
        score_data = scoresCollection.find_one({"_id.scorerUserId": data['facebookId'],
                                                "_id.buy_id": data["buyId"]},)
        scoresCollection.update_one({"_id": {"scorerUserId": data['facebookId'],
                                             "buy_id": data["buyId"]}},
                                    {'$set': {"value": data['value'],
                                              "comment": data['comment']}})
        try:
            return score_data["scoredUserId"]
        except Exception:
            return None

    @staticmethod
    def find_score_by_scorer_id(data):
        return list(scoresCollection.find({"_id.scorerUserId": data}))

    @staticmethod
    def find_score_by_scored_id(data):
        return list(scoresCollection.find({"scoredUserId": data}))

    @staticmethod
    def find_score(data):
        return scoresCollection.find_one({"_id": {"scorerUserId": data['facebookId'],
                                                  "buy_id": data["buyId"]}})

    @staticmethod
    def find_scored_user_average(user_id):

            pipeline = [
                {
                    u"$match": {
                        u"scoredUserId": user_id
                    }
                },
                {
                    u"$group": {
                        u"_id": {},
                        u"AVG(value)": {
                            u"$avg": u"$value"
                        }
                    }
                },
                {
                    u"$project": {
                        u"_id": 0,
                        u"AVG(value)": u"$AVG(value)"
                    }
                }
            ]

            cursor = scoresCollection.aggregate(
                pipeline,
                allowDiskUse=True
            )
            try:
                return list(cursor)[0]["AVG(value)"]
            except Exception:
                return None

    @staticmethod
    def __get_calificado(data):
        buy = BuyTransactions.findBuyById(data["buyId"])
        seller_facebook_id = PostTransactions.find_post_by_post_id(buy["postId"])["_id"]["facebookId"]
        buyer_facebook_id = buy["_id"]["facebookId"]
        if data["rol"] == "Vendedor":
            data["estado"] = ESTADO_COMPLETADO
            UserTransactions.updateUserSellPoints(seller_facebook_id)
            BuyTransactions.updateBuyData(data)
            return buyer_facebook_id
        else:
            data["estado"] = ESTADO_CALIFICADO
            UserTransactions.updateUserBuyPoints(buyer_facebook_id, buy["paymentMethod"])
            BuyTransactions.updateBuyData(data)
            return seller_facebook_id

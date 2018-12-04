from server.Communication.DatabaseCommunication.buyTransactions import BuyTransactions
from server.Communication.DatabaseCommunication.postTransactions import PostTransactions
from server.setup import app
import logging
import json
import datetime
import time
from server.Communication.SharedServerCommunication.sharedServerRequests import SharedServerRequests


logging.basicConfig(filename='debug.log', level=logging.DEBUG)
with app.app_context():
    scoresCollection = app.database.scores


class ScoreTransactions:

    def __init__(self):
        pass

    @staticmethod
    def create_new_score(data):

        calificado = ScoreTransactions.__get_calificado(data)
        insert_data = data.copy()
        insert_data.pop("facebookId", None)
        insert_data.pop("token", None)
        if insert_data["comment"] is None:
            insert_data["comment"] = ""

        scoresCollection.insert_one({"_id": {"scorerUserId": data['facebookId'],
                                             "buy_id": data["buyId"]}})
        scoresCollection.update_one({"_id": {"scorerUserId": data['facebookId'],
                                             "buy_id": data["buyId"]}},
                                    {'$set': {"scoredUserId": calificado,
                                              "value": data['value'],
                                              "comment": data['comment']}})
        return calificado
    @staticmethod
    def update_score(data):
        score_id = scoresCollection.update_one({"_id": {"scorerUserId": data['facebookId'],
                                                "buy_id": data["buyId"]}},
                                               {'$set': {"value": data['value'],
                                                         "comment": data['comment']}})
        return score_id

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
        return list(cursor)[0]["AVG(value)"]

    @staticmethod
    def __get_calificado(data):
        buy = BuyTransactions.findBuyerById(data["buyId"])
        if data["rol"] == "Vendedor":
            return buy["_id"]["facebookId"]
        else:
            id = PostTransactions.find_post_by_post_id(buy["postId"])["_id"]["facebookId"]
            logging.debug(id)
            logging.debug(data['buyId'])
            return id

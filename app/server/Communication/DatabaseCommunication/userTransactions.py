from server.setup import app
from flask import Flask
import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG)
with app.app_context():
    userCollection = app.database.users

SCORE_MULTIPLIER = 100
BUY_SCORE = 20
SELL_SCORE = 20
CARD_POINTS = 5
MERCADO_PAGO_POINTS = 10
CASH_POINTS = 0

class UserTransactions:

    def __init__(self):
        pass

    @staticmethod
    def __parseUpdateData(data):
        parsed_data = {}
        if "firstName" in data.keys():
            parsed_data["nombre"] = data["firstName"]
        if "lastName" in data.keys():
            parsed_data["apellido"] = data["lastName"]
        if "photoUrl" in data.keys():
            parsed_data["photoUrl"] = data["photoUrl"]
        if "email" in data.keys():
            parsed_data["email"] = data["email"]
        return parsed_data

    @staticmethod
    def findUserById(facebook_id):
        return userCollection.find_one({'facebookId': facebook_id})

    @staticmethod
    def getUserName(facebook_id):
        return userCollection.find_one({'facebookId': facebook_id}, {"nombre": 1, "apellido": 1, "_id": 0})

    @staticmethod
    def newUser(user_id, first_name, last_name, photo_url, email):

        id = userCollection.insert_one({"facebookId": user_id,
                                           "nombre": first_name,
                                           "apellido": last_name,
                                           "photoUrlToken": photo_url,
                                           "email": email})
        return id

    @staticmethod
    def updateUserToken(facebook_id, new_token, new_expdate):
        userCollection.update_one({'facebookId': facebook_id},
                                     {'$set': {'token': new_token, 'exp_date': new_expdate}})

    @staticmethod
    def updateUserBuyPoints(facebook_id, payment_method):
        points = BUY_SCORE
        if payment_method == "Debito" or payment_method == "Credito":
            points += CARD_POINTS
        elif payment_method == "Efectivo" \
                or payment_method == "Transferencia" \
                or payment_method == "Cheque"\
                or payment_method == "DepositoBancario":
            points += CASH_POINTS
        elif payment_method == "MercadoPago":
            points += MERCADO_PAGO_POINTS
        userCollection.update_one({'facebookId': facebook_id},
                                     {'$set': {'$inc': {'buyPoints': points}}})
        UserTransactions.__update_total_score(facebook_id)

    @staticmethod
    def updateUserSellPoints(facebook_id):
        points = SCORE_MULTIPLIER
        userCollection.update_one({'facebookId': facebook_id},
                                     {'$set': {'$inc': {'sellPoints': points}}})
        UserTransactions.__update_total_score(facebook_id)

    @staticmethod
    def updateUserScorePoints(facebook_id, score_average):
        points = int(score_average*100)
        logging.debug(facebook_id)
        logging.debug(points)
        userCollection.update_one({'facebookId': facebook_id},
                                     {'$set': {'scorePoints': points}})
        UserTransactions.__update_total_score(facebook_id)


    @staticmethod
    def updateUserData(data):
        parsed_data = UserTransactions.__parseUpdateData(data)
        if parsed_data:
            userCollection.update_one({'facebookId': data['facebookId']}, {'$set': parsed_data})

    @staticmethod
    def getUserActivities(facebook_id):
        return userCollection.find_one({'facebookId': facebook_id}, {"activities": 1})

    @staticmethod
    def pushUserActivitiy(facebook_id, data):
        return userCollection.update_one({'facebookId': facebook_id}, {'$set': {'$push': {'activities': data}}})

    @staticmethod
    def __update_total_score(facebook_id):
        result = userCollection.find_one({'facebookId': facebook_id},
                                         {"sellPoints": 1, "buyPoints": 1, "scorePoints": 1})
        if "sellPoints" not in result.keys():
            result["sellPoints"] = 0
        if "buyPoints" not in result.keys():
            result["buyPoints"] = 0
        if "scorePoints" not in result.keys():
            result["scorePoints"] = 0
        points = result["sellPoints"]
        points += result["buyPoints"]
        points += result["scorePoints"]
        userCollection.update_one({'facebookId': facebook_id}, {'$set': {'totalPoints': points}})

"""    @staticmethod
    def __getCalification(facebook_id):
        BuyTransactions.findBuyCalificationAverageByUserId(facebook_id)
        return 10"""
from server.setup import app
from flask import Flask
import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG)
with app.app_context():
    workingCollection = app.database.users


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
        return workingCollection.find_one({'facebookId': facebook_id})

    @staticmethod
    def getUserName(facebook_id):
        return workingCollection.find_one({'facebookId': facebook_id}, {"nombre": 1, "apellido": 1, "_id": 0})

    @staticmethod
    def newUser(user_id, first_name, last_name, photo_url, email):

        id = workingCollection.insert_one({"facebookId": user_id,
                                           "nombre": first_name,
                                           "apellido": last_name,
                                           "photoUrlToken": photo_url,
                                           "email": email})
        return id

    @staticmethod
    def updateUserToken(facebook_id, new_token, new_expdate):
        workingCollection.update_one({'facebookId': facebook_id},
                                     {'$set': {'token': new_token, 'exp_date': new_expdate}})

    @staticmethod
    def updateUserBuyPoints(facebook_id, payment_method):
        points = 0
        if payment_method == "":
            points = 0
        elif payment_method == "":
            points = 0
        elif payment_method == "":
            points = 0
        elif payment_method == "":
            points = 0
        workingCollection.update_one({'facebookId': facebook_id},
                                     {'$set': {'$inc': {'buyPoints': points, 'totalPoints': points}}})

    @staticmethod
    def updateUserSellPoints(facebook_id):
        points = 0
        workingCollection.update_one({'facebookId': facebook_id},
                                     {'$set': {'$inc': {'sellPoints': points, 'totalPoints': points}}})

    @staticmethod
    def updateUserCalificationPoints(facebook_id, calification):
        points = calification*100
        workingCollection.update_one({'facebookId': facebook_id},
                                     {'$set': {'calificationPoints': points}})
        workingCollection.update_one({'facebookId': facebook_id},
                                     {'$set': {'totalPoints': {'$add':
                                                                   ['sellPoints', 'buyPoints', 'calificationPoints']}}})

    @staticmethod
    def updateUserData(data):
        parsed_data = UserTransactions.__parseUpdateData(data)
        if parsed_data:
            workingCollection.update_one({'facebookId': data['facebookId']}, {'$set': parsed_data})

    @staticmethod
    def getUserActivities(facebook_id):
        return workingCollection.find_one({'facebookId': facebook_id}, {"activities": 1})

    @staticmethod
    def pushUserActivitiy(facebook_id, data):
        return workingCollection.update_one({'facebookId': facebook_id}, {'$set': {'$push': {'activities': data}}})

"""    @staticmethod
    def __getCalification(facebook_id):
        BuyTransactions.findBuyCalificationAverageByUserId(facebook_id)
        return 10"""
from server.setup import app
from flask import Flask
with app.app_context():
    workingCollection = app.database.users


class UserTransactions:

    def __init__(self):
        pass

    @staticmethod
    def findUserById(facebook_id):
        return workingCollection.find_one(facebook_id)

    @staticmethod
    def newUser(user, token, exp_date):
        return workingCollection.insert_one({'facebookId': user, 'token': new_token, 'exp_date': new_expdate})

    @staticmethod
    def updateUserToken(facebookId, new_token, new_expdate):
        workingCollection.update_one({{'facebookId': facebookId}, {'$set': {'token': new_token, 'exp_date': new_expdate}}})


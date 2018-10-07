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
    def findUserById(facebook_id):
        return workingCollection.find_one({'facebookId': facebook_id})

    @staticmethod
    def newUser(user):
        logging.debug("DB debug:" + str({'facebookId': user}))

        return workingCollection.insert_one({'facebookId': user})

    @staticmethod
    def updateUserToken(facebookId, new_token, new_expdate):
        workingCollection.update_one({'facebookId': facebookId}, {'$set': {'token': new_token, 'exp_date': new_expdate}})


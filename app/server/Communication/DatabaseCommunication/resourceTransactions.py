from server.logger import Logger
from server.setup import app

LOGGER = Logger.get(__name__)
with app.app_context():
    categoriesCollection = app.database.categories
    paymentsCollection = app.database.payments
    buyStatesCollection = app.database.buy_states


class ResourceTransactions:

    def __init__(self):
        pass

    @staticmethod
    def get_categories():
        return list(categoriesCollection.find())

    @staticmethod
    def get_payments():
        return list(paymentsCollection.find())

    @staticmethod
    def get_buys_states():
        return list(buyStatesCollection.find())

    @staticmethod
    def get_buy_states_by_id(state_id):
        result = buyStatesCollection.find_one({"_id": state_id}, {"tracking": 0, "payment": 0, "_id": 0})
        return result
    @staticmethod
    def get_buy_tracking_states_by_id(state_id):
        return buyStatesCollection.find_one({"_id": state_id, "tracking": True}, {"tracking": 0, "_id": 0})

    @staticmethod
    def get_buy_payment_states_by_id(state_id):
        return buyStatesCollection.find_one({"_id": state_id, "payment": True}, {"payment": 0, "_id": 0})

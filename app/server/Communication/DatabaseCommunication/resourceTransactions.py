from server.setup import app
import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG)
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
    def get_buys_states_ids():
        return list(buyStatesCollection.find({},{"estado": 0}))

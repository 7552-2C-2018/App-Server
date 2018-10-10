from server.setup import app
import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG)
with app.app_context():
    categoriesCollection = app.database.categories
    paymentsCollection = app.database.payments


class ProductTransactions:

    def __init__(self):
        pass

    @staticmethod
    def get_categories():
        return list(categoriesCollection.find())

    @staticmethod
    def get_payments():
        return list(paymentsCollection.find())

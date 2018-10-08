from server.setup import app
from flask import Flask
import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG)
with app.app_context():
    categoriesCollection = app.database.categories


class ProductTransactions:

    def __init__(self):
        pass

    @staticmethod
    def getCategories():
        return list(categoriesCollection.find())

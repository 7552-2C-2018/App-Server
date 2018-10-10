import json
from server.Structures.Response import Responses
from server.Communication.DatabaseCommunication.productTransactions import ProductTransactions
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


class ProductServices:

    def __init__(self):
        pass

    @staticmethod
    def get_categories():
        return Responses.success("Categorias obtenidas satisfactoriamente", ProductTransactions.get_categories())

    @staticmethod
    def get_payments():
        return Responses.success("Formas de pago obtenidas satisfactoriamente", ProductTransactions.get_payments())

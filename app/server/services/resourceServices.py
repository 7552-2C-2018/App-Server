import json
from server.Structures.Response import Responses
from server.Communication.DatabaseCommunication.resourceTransactions import ResourceTransactions
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


class ResourcesServices:

    def __init__(self):
        pass

    @staticmethod
    def get_categories():
        return Responses.success("Categorias obtenidas satisfactoriamente", ResourceTransactions.get_categories())

    @staticmethod
    def get_payments():
        return Responses.success("Formas de pago obtenidas satisfactoriamente", ResourceTransactions.get_payments())

    @staticmethod
    def get_buy_states():
        return Responses.success("Estados posibles de las compras satisfactoriamente",
                                 ResourceTransactions.get_buys_states())

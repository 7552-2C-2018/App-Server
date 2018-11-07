from server.Structures.Response import Responses
from server.Communication.DatabaseCommunication.buyTransactions import BuyTransactions
from server.Communication.DatabaseCommunication.userTransactions import UserTransactions
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


class BuyServices:

    @staticmethod
    def getAllBuys():
        response = BuyTransactions.getBuys()
        return Responses.success('Compras obtenidos satisfactoriamente', response)

    @staticmethod
    def getBuy(request_data):
        response = BuyTransactions.findBuyById(request_data["buyId"])

        if not response is None:
            #response["name"] = UserTransactions.getUserName(response["_id"]["facebookId"])
            return Responses.success('Compras obtenidos satisfactoriamente', response)
        else:
            return Responses.badRequest('Compras inexistente')

    @staticmethod
    def getBuyByUser(request_data):
        response = BuyTransactions.findBuyByUserId(request_data["userId"])

        if not response is None:
            return Responses.success('Compras obtenidos satisfactoriamente', response)
        else:
            return Responses.badRequest('Usuario sin Compras')

    @staticmethod
    def getBuyBySeller(request_data):
        response = BuyTransactions.findBuyBySellerId(request_data["seller_id"])

        if not response is None:
            return Responses.success('Compras obtenidos satisfactoriamente', response)
        else:
            return Responses.badRequest('Usuario sin Compras')

    @staticmethod
    def createNewBuy(request_data):
        BuyTransactions.newBuy(request_data)
        return Responses.created('Compras creada satisfactoriamente', "")

    @staticmethod
    def updateBuy(request_data):
        response = BuyTransactions.updateBuyData(request_data)
        if response != "Estado Invalido":
            return Responses.success('Compra actualizada satisfactoriamente', "")
        else:
            return Responses.badRequest('Estado Invalido')



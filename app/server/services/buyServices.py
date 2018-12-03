from server.Structures.Response import Responses
from server.Communication.DatabaseCommunication.buyTransactions import BuyTransactions
from server.Communication.DatabaseCommunication.postTransactions import PostTransactions
from server.Communication.FirebaseCommunication.firebaseCommunication import FirebaseCommunication
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


class BuyServices:

    @staticmethod
    def getAllBuys():
        response = BuyTransactions.getBuys()
        return Responses.success('Compras obtenidas satisfactoriamente', response)

    @staticmethod
    def getBuy(request_data):

        response = BuyTransactions.findBuyById(request_data["buyId"])

        if not response is None:
            #response["name"] = UserTransactions.getUserName(response["_id"]["facebookId"])
            return Responses.success('Compras obtenidas satisfactoriamente', response)
        else:
            return Responses.badRequest('Compras inexistente')

    @staticmethod
    def getBuysByUser(request_data):

        response = BuyTransactions.findBuyByUserId(request_data["userId"])
        if not response is None:
            return Responses.success('Compras obtenidas satisfactoriamente', response)
        else:
            return Responses.badRequest('Usuario sin Compras')

    @staticmethod
    def getBuysBySeller(request_data):
        response = BuyTransactions.findBuyBySellerId(request_data["seller_id"])

        if not response is None:
            logging.debug("dasdasd" + str(response))
            return Responses.success('Compras obtenidas satisfactoriamente', response)
        else:
            return Responses.badRequest('Usuario sin Compras')

    @staticmethod
    def createNewBuy(request_data):
        try:
            BuyTransactions.newBuy(request_data)
            post_data = PostTransactions.find_post_by_post_id(request_data['postId'])
            FirebaseCommunication.new_chat(request_data['facebookId'], post_data)
            return Responses.created('Compra creada satisfactoriamente', "")
        except Exception:
            return Responses.internalServerError('Error en la comunicacion con el sharedServer')

    @staticmethod
    def updateBuy(request_data):
        response = BuyTransactions.updateBuyData(request_data)
        if response != "Estado Invalido":
            return Responses.success('Compra actualizada satisfactoriamente', "")
        else:
            return Responses.badRequest('Estado Invalido')




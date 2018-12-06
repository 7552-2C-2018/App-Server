from server.logger import Logger
from server.Communication.DatabaseCommunication.userTransactions import UserTransactions
from server.Structures.Response import Responses
from server.Communication.DatabaseCommunication.buyTransactions import BuyTransactions
from server.Communication.DatabaseCommunication.postTransactions import PostTransactions
from server.Communication.FirebaseCommunication.firebaseCommunication import FirebaseCommunication

LOGGER = Logger.get(__name__)


class BuyServices:

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
        response = BuyTransactions.find_buy_by_seller_id(request_data["seller_id"])

        if not response is None:
            return Responses.success('Compras obtenidas satisfactoriamente', response)
        else:
            return Responses.badRequest('Usuario sin Compras')

    @staticmethod
    def createNewBuy(request_data):
        try:
            BuyTransactions.newBuy(request_data)
        except Exception:
            return Responses.internalServerError('Error en la comunicacion con el sharedServer')
        post_data = PostTransactions.find_post_by_post_id(request_data['postId'])
        FirebaseCommunication.new_chat(request_data['facebookId'], post_data)
        UserTransactions.pushUserActivitiy(request_data['facebookId'], "Has realizado una compra")
        UserTransactions.pushUserActivitiy(post_data['_id']['facebookId'], "Has realizado una venta")
        FirebaseCommunication.send_notification(post_data['_id']['facebookId'], "Has realizado una venta",
                                                post_data["title"])
        return Responses.created('Compra creada satisfactoriamente', "")


    @staticmethod
    def updateBuy(request_data):
        LOGGER.debug("Req data:" + str(request_data))
        if BuyServices.__validate_buy(request_data):
            return Responses.badRequest('Compra inexistente')
        #try:
        response = BuyTransactions.updateBuyData(request_data)
        return Responses.success('Compra actualizada satisfactoriamente', "")
        #except Exception:
        return Responses.badRequest('Estado Invalido')

    @staticmethod
    def update_buy_by_payment_id(request_data):
        if BuyServices.__validate_buy(request_data):
            return Responses.badRequest('Compra inexistente')
        response = BuyTransactions.update_buy_by_payment_id(request_data)
        if response != "Estado Invalido":
            return Responses.success('Compra actualizada satisfactoriamente', "")
        else:
            return Responses.badRequest('Estado Invalido')

    @staticmethod
    def update_buy_by_tracking_id(request_data):
        if BuyServices.__validate_buy(request_data):
            return Responses.badRequest('Compra inexistente')
        response = BuyTransactions.update_buy_by_tracking_id(request_data)
        if response != "Estado Invalido":
            return Responses.success('Compra actualizada satisfactoriamente', "")
        else:
            return Responses.badRequest('Estado Invalido')

    @staticmethod
    def __validate_buy(request_data):
        valid_buy = BuyTransactions.find_buy(request_data["buyId"])
        return valid_buy is None




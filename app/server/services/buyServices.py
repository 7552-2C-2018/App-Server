from server.Communication.DatabaseCommunication.userTransactions import UserTransactions
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
        except Exception:
            return Responses.internalServerError('Error en la comunicacion con el sharedServer')
        post_data = PostTransactions.find_post_by_post_id(request_data['postId'])
        FirebaseCommunication.new_chat(request_data['facebookId'], post_data)
        buy_data = BuyServices.__generate_buy_activiy_data(request_data)
        sell_data = BuyServices.__generate_sell_activiy_data(post_data)
        UserTransactions.pushUserActivitiy(request_data['facebookId'], buy_data)
        UserTransactions.pushUserActivitiy(post_data['facebookId'], sell_data)
        return Responses.created('Compra creada satisfactoriamente', "")


    @staticmethod
    def updateBuy(request_data):
        response = BuyTransactions.updateBuyData(request_data)
        if response != "Estado Invalido":
            return Responses.success('Compra actualizada satisfactoriamente', "")
        else:
            return Responses.badRequest('Estado Invalido')

    @staticmethod
    def update_buy_by_payment_id(request_data):
        response = BuyTransactions.update_buy_by_payment_id(request_data)
        if response != "Estado Invalido":
            return Responses.success('Compra actualizada satisfactoriamente', "")
        else:
            return Responses.badRequest('Estado Invalido')

    @staticmethod
    def update_buy_by_tracking_id(request_data):
        response = BuyTransactions.update_buy_by_tracking_id(request_data)
        if response != "Estado Invalido":
            return Responses.success('Compra actualizada satisfactoriamente', "")
        else:
            return Responses.badRequest('Estado Invalido')

    @staticmethod
    def __generate_buy_activiy_data(data):
        return {"action": "buy", "buy": data["buyId"]}

    @staticmethod
    def __generate_sell_activiy_data(data):
        return {"sell": "buy", "post": data["ID"]}



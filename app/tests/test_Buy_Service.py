from . import GenericTest
from server.setup import app
from server.services.buyServices import BuyServices
from unittest.mock import *
PAYMENT_STATE_CODE = 7
TRACKING_STATE_CODE = 11
registered_credentials = {"facebookId": "102510700706087", "token": ""}
registered_credentials_with_date = {"facebookId": "102510700706087", "token": "", "postId": "1025107007060871539228792"}
new_buy_data = {"facebookId": "102510700706087",
                "postId": "1025107007060871539228792",
                "category": "test",
                "street": "calle falsa 123",
                "cardNumber": 1111,
                "price": 100,
                "paymentMethod": "Efectivo"
                 }

common_update_buy_data = {"facebookId": "102510700706087",
                   "buyId": "991539228792",
                   "estado": "1"}


@patch('server.Communication.SharedServerCommunication.sharedServerRequests.'
       'SharedServerRequests.newPayment',
       MagicMock(return_value=1))
@patch('server.Communication.SharedServerCommunication.sharedServerRequests.'
       'SharedServerRequests.newTracking',
       MagicMock(return_value=1))
@patch('server.Communication.FirebaseCommunication.firebaseCommunication.'
       'FirebaseCommunication.new_chat', MagicMock())
@patch('server.Communication.FirebaseCommunication.firebaseCommunication.'
       'FirebaseCommunication.send_notification', MagicMock())
@patch('server.Communication.GeolocationServiceCommunication.geolocationServiceCommunication.'
       'GeolocationServiceCommunication.getCoordenates', MagicMock(return_value=1))
class BuyTests(GenericTest):

    def test_get_buy_id(self):
        user_credentials = {"userId": "102510700706087", "token": "", "buyId": "991539228792"}
        response = BuyServices.getBuy(user_credentials)
        assert response["message"] == 'Compras obtenidas satisfactoriamente'
        assert response["status"] == 200

    def test_get_buy_user(self):
        user_credentials = {"userId": "102510700706087", "token": ""}
        response = BuyServices.getBuysByUser(user_credentials)
        assert response["message"] == 'Compras obtenidas satisfactoriamente'
        assert response["status"] == 200

    def test_get_buy_seller(self):
        seller_credentials = {"seller_id": "102510700706087", "token": ""}
        response = BuyServices.getBuysBySeller(seller_credentials)
        assert response["message"] == 'Compras obtenidas satisfactoriamente'
        assert response["status"] == 200

    def test_new_buy_id(self):
        response = BuyServices.createNewBuy(new_buy_data)
        assert response["message"] == 'Compra creada satisfactoriamente'
        assert response["status"] == 201

    def test_update_buy_user(self):
        update_buy_data = common_update_buy_data.copy()
        response = BuyServices.updateBuy(update_buy_data)
        assert response["message"] == 'Compra actualizada satisfactoriamente'
        assert response["status"] == 200

    def test_update_not_existing_buy_user(self):
        update_buy_data = common_update_buy_data.copy()
        update_buy_data["buyId"] = "2"
        response = BuyServices.updateBuy(update_buy_data)
        assert response["message"] == 'Compra inexistente'
        assert response["status"] == 400

    def test_update_buy_by_user_with_external_payment(self):
        update_buy_data = common_update_buy_data.copy()
        update_buy_data["estado"] = PAYMENT_STATE_CODE
        update_buy_data["buyId"] = "991539228999"
        response = BuyServices.updateBuy(update_buy_data)
        assert response["message"] == 'Estado Invalido'
        assert response["status"] == 400

    def test_update_buy_by_user_with_external_tracking(self):
        update_buy_data = common_update_buy_data.copy()
        update_buy_data["estado"] = TRACKING_STATE_CODE
        update_buy_data["buyId"] = "991539228999"
        response = BuyServices.updateBuy(update_buy_data)
        assert response["message"] == 'Estado Invalido'
        assert response["status"] == 400

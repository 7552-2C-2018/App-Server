from . import GenericTest
from server.setup import app
from server.services.buyServices import BuyServices
from unittest.mock import *

registered_credentials = {"facebookId": "102510700706087", "token": ""}
registered_credentials_with_date = {"facebookId": "102510700706087", "token": "", "postId": "1025107007060871539228792"}
new_buy = {"facebookId": "102510700706087",
            "category": "test",
            "coordenates": [
                12,
                13
            ],
            "description": "Desde swagger",
            "new": True,
            "payments": [
                "EFECTIVO"
            ],
            "pictures": None,
            "price": 10,
            "shipping": False,
            "stock": 2,
            "title": "Prueba"}

"""
class PostsTests(GenericTest):

    def test_get_all_buys(self):
        response = BuyServices.getAllBuys(registered_credentials_with_date)
        assert response["status"] == 200
        assert response["message"] == 'Compras obtenidas satisfactoriamente'

    def test_get_buy_id(self):
        response = BuyServices.findBuyByUserId(registered_credentials_with_date)
        assert response["status"] == 200
        assert response["message"] == 'Compras obtenidas satisfactoriamente'

    def test_get_buy_user(self):
        response = BuyServices.findBuyByUserId(registered_credentials_with_date)
        assert response["status"] == 200
        assert response["message"] == 'Compras obtenidas satisfactoriamente'

    def test_get_buy_seller(self):
        response = BuyServices.getBuysBySeller(registered_credentials_with_date)
        assert response["status"] == 200
        assert response["message"] == 'Compras obtenidas satisfactoriamente'

    @patch('server.Communication.sharedServerCommunication.newPayment',
           MagicMock(return_value=1))
    def test_new_buy_id(self):
        response = BuyServices.createNewBuy(new_buy)
        assert response["status"] == 201
        assert response["message"] == 'Compra creada satisfactoriamente'

    def test_update_buy(self):
        response = BuyServices.updateBuy(new_buy)
        assert response["status"] == 201
        assert response["message"] == 'Compra actualizada satisfactoriamente'
"""
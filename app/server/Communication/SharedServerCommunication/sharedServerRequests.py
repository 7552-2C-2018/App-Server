import requests
import json
SERVER_ID = 6
SHARED_SERVER_URL = 'https://shared-server-25.herokuapp.com'


class SharedServerRequests:

    def __init__(self):
        self.token = SharedServerRequests.__auth()

    @staticmethod
    def __auth():
        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'}
        response = requests.post(SHARED_SERVER_URL + '/api/auth/token', headers=json.dumps(headers), json=json.dumps({'id': SERVER_ID}))
        if response.status_code == 201:
            return json.loads(response.text)
        return ""

    @staticmethod
    def newPayment(data):
        token = SharedServerRequests.__auth()
        response = requests.post(SHARED_SERVER_URL + '/api/payment', headers={'x-access-token': token}, json=json.dumps(data))
        if response.status_code == 20:
            return json.loads(response.text)
        else:
            return None

    @staticmethod
    def newShipping(data):
        token = SharedServerRequests.__auth()
        response = requests.post(SHARED_SERVER_URL + '/api/tracking', headers={'x-access-token': token}, json=json.dumps(data))
        if response.status_code == 20:
            return json.loads(response.text)
        else:
            return None

    @staticmethod
    def getPayment(id):
        token = SharedServerRequests.__auth()
        response = requests.post(SHARED_SERVER_URL + '/api/payment/' + str(id), headers={'x-access-token': token})
        if response.status_code == 201:
            return json.loads(response.text)
        else:
            return None

    @staticmethod
    def getShipping(id):
        token = SharedServerRequests.__auth()
        response = requests.post(SHARED_SERVER_URL + '/api/deliveries/' + str(id), headers={'x-access-token': token})
        if response.status_code == 201:
            return json.loads(response.text)
        else:
            return None

    @staticmethod
    def calculateShipping(shippingData):
        """token = SharedServerRequests.__auth()
        response = requests.get(SHARED_SERVER_URL + '/api/deliveries/estimate', header={'x-access-token': token}, json=json)

        if response.status_code == 201:
            return json.loads(response.text)
        else:
            return None"""
        return {"Precio envio": 100}
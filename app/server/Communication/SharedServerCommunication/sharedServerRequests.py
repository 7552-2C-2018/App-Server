from urllib.parse import urlencode, quote

import requests
import json
from math import sin, cos, sqrt, atan2, radians
from server.Communication.DatabaseCommunication.postTransactions import PostTransactions
from server.Communication.GeolocationServiceCommunication.geolocationServiceCommunication import \
    GeolocationServiceCommunication
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)
SERVER_ID = "7"
SHARED_SERVER_URL = 'https://shared-server-25.herokuapp.com'


class SharedServerRequests:

    def __init__(self):
        self.token = SharedServerRequests.__auth()

    @staticmethod
    def __auth():
        headers = {}
        headers['Content-Type'] = "application/json"
        headers['Accept'] = "application/json"
        response = requests.post(SHARED_SERVER_URL + '/api/auth/token', headers=headers, data=json.dumps({"id": SERVER_ID}))
        logging.debug("token: " + str(response))
        if response.status_code == 201:
            headers['x-access-token'] = json.loads(response.text)["token"]
            return headers
        return None

    @staticmethod
    def __parsePayment(data, post):
        payment_data = {}
        date = data["cardDate"].split("/")
        payment_data["number"] = data["cardNumber"]
        payment_data["value"] = data["price"]
        payment_data["expiration_year"] = "20" + date[1]
        payment_data["expiration_month"] = date[0]
        payment_data["currency"] = "ars"
        payment_data["type"] = data["cardBank"]
        payment_data["ownerId"] = data["cardBank"]
        return payment_data

    @staticmethod
    def newPayment(data, post):
        headers = (SharedServerRequests.__auth())
        payment_data = SharedServerRequests.__parsePayment(data,post)
        response = requests.post(SHARED_SERVER_URL + '/api/payments', headers=headers,
                                 data=json.dumps(payment_data))
        logging.debug("payment data: " + json.dumps(payment_data))
        logging.debug("payment req: " + str(response.text))
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None

    @staticmethod
    def __parseTracking(data, post):
        try:
            tracking_data = {}
            tracking_data["ownerId"] = post["ID"]
            tracking_data["start_time"] = ""
            tracking_data["start_street"] = ""
            tracking_data["start_lat"] = post["coordenates"][0]
            tracking_data["start_lon"] = post["coordenates"][1]
            tracking_data["end_time"] = ""
            tracking_data["end_street"] = data["street"] + " " + data["floor"] + \
                                          " " + data["dept"] + ", " + data["city"]
            end_coordenates = GeolocationServiceCommunication.getCoordenates(data["street"], data["city"])
            tracking_data["end_lat"] = float(end_coordenates["latitud"])
            tracking_data["end_lon"] = float(end_coordenates["longitud"])
            tracking_data["distance"] = SharedServerRequests.__calulateDistance(post["coordenates"],end_coordenates)
            tracking_data["currency"] = "ars"
            tracking_data["value"] = data["price"]
            logging.debug("end_coordenates data: " + str(tracking_data))
        except Exception as e:
            logging.debug(str(e))
            return None
        return tracking_data

    @staticmethod
    def __calulateDistance(coordenatesList, coordenatesDict):
        try:
            R = 6373.0

            lat1 = radians(coordenatesList[1])
            lon1 = radians(coordenatesList[0])
            lat2 = radians(float(coordenatesDict["latitud"]))
            lon2 = radians(float(coordenatesDict["longitud"]))

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c
        except Exception as e:
            logging.debug(str(e))
            raise Exception

    @staticmethod
    def newTracking(data, post):
        try:
            headers = (SharedServerRequests.__auth())
            tracking_data = SharedServerRequests.__parseTracking(data, post)
            logging.debug("track data: " + json.dumps(tracking_data))
            response = requests.post(SHARED_SERVER_URL + '/api/tracking', headers=headers,
                                     data=json.dumps(tracking_data))
            logging.debug("track req: " + str(response.text))
        except Exception as e:
            logging.debug(str(e))
            return None
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None

    @staticmethod
    def getPayment(id):
        headers = (SharedServerRequests.__auth())
        response = requests.post(SHARED_SERVER_URL + '/api/payment/' + str(id), headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None

    @staticmethod
    def getTracking(id):
        headers = (SharedServerRequests.__auth())
        response = requests.post(SHARED_SERVER_URL + '/api/tracking/' + str(id), headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None

    @staticmethod
    def calculateShipping(shippingData):
        headers = (SharedServerRequests.__auth())
        response = requests.get(SHARED_SERVER_URL + '/api/deliveries/estimate', headers=headers, json=json)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return None

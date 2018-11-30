import requests
import json
from threading import Thread
from functools import wraps
import datetime
import time

URL = 'http://servicios.usig.buenosaires.gob.ar/'
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


class GeolocationServiceCommunication:

    @staticmethod
    def getCoordenates(calle,localidad):
        logging.debug("entro " )
        response = requests.get(URL + 'normalizar/?direccion='+calle+','+localidad+'&geocodificar=TRUE&maxOptions=1')
        logging.debug("coordenadas: " + str(response.text))
        coordenadas = json.loads(response.text)["direccionesNormalizadas"][0]["coordenadas"]

        return {"latitud": coordenadas["y"], "longitud": coordenadas["x"]}


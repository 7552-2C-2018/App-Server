import requests
import json
from threading import Thread
from functools import wraps
import datetime
import time

from server.logger import Logger

URL = 'http://servicios.usig.buenosaires.gob.ar/'

LOGGER = Logger().get(__name__)


class GeolocationServiceCommunication:

    @staticmethod
    def getCoordenates(calle,localidad):
        LOGGER.info("Inicio de comunicacion con USIG")
        response = requests.get(URL + 'normalizar/?direccion='+calle+','+localidad+'&geocodificar=TRUE&maxOptions=1')
        LOGGER.info("Geolocalizado: " + str(response.text))
        try:
            coordenadas = json.loads(response.text)["direccionesNormalizadas"][0]["coordenadas"]
            return {"latitud": coordenadas["y"], "longitud": coordenadas["x"]}
        except:
            LOGGER.warn("Error de USIG al geolocalizar")
            return None

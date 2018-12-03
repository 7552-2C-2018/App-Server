import logging
import os


class Logger(object):
    LEVEL = os.environ.get('NIVEL_LOGGING')
    if not LEVEL:
        LEVEL = 'DEBUG'
    logging.basicConfig(level=LEVEL)

    @staticmethod
    def get(name):
        logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H-%M-%S')
        return logging.getLogger(name)

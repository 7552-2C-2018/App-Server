import datetime
import logging
import asyncio
import time
from functools import wraps
from threading import Thread


from server.setup import app

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

with app.app_context():
    monitor_collection = app.database.stats


def monitor(time_start, time_end, path, method):
    monitor_data(path, method, time_end, time_start)

def monitor_data(path, method, time_end, time_start):
    logging.debug("estamo aca 2")
    request_data = {
        'route': path,
        'method': method,
        'date_time': datetime.datetime.utcnow(),
        'day': time.strftime('%d/%m/%Y'),
        'hour': time.strftime('%H'),
        'time_elapsed_ms': int((time_end - time_start) * 1000)
    }
    monitor_collection.insert_one(request_data)



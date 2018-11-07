import requests
import json
from threading import Thread
from functools import wraps
import datetime
import time

URL = 'https://melli-7552.firebaseio.com/'
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

def async_f(function):

    @wraps(function)
    def async_func(*args, **kwargs):
        thrd = Thread(target=async_func, args=args, kwargs=kwargs)
        thrd.start()
        return thrd
    return async_func


class FirebaseCommunication:

    @staticmethod
    @async_f
    def __newUserChat(facebook_id, chat_key):
        user = requests.get(URL + 'userChats/' + facebook_id + '.json')
        if user.text == "null":
            dict = {
                facebook_id: {'chats':[]}
            }
            requests.put(URL + 'userChats.json', data=json.dumps(dict))
        chats = requests.get(URL + 'userChats/' + facebook_id + '/chats.json')
        if chats.text != "null":
            new_chat_list = json.loads(chats.text)
            new_chat_list.append(chat_key)
            logging.debug(str(new_chat_list))
        else:
            new_chat_list = [chat_key]
        requests.put((URL + 'userChats/' + facebook_id + '.json'), data=json.dumps({'chats': new_chat_list}))

    @staticmethod
    @async_f
    def __newUser(data):
        facebook_id = data['facebookId']
        data.pop('facebookId')
        dict = {
                facebook_id: data
            }
        requests.put(URL + 'user/' + facebook_id + '.json', data=json.dumps(dict))

    @staticmethod
    @async_f
    def newChat(facebook_id_comprador, post_data):
        payload = {
                "picture": post_data["pictures"],
                "title": post_data["title"],
                "publicationId": post_data["ID"],
                "messages": {"0":{"senderId": post_data["_id"]["facebookId"],
                                  "text": "Gracias por su compra!",
                                  "timestamp": time.mktime(datetime.datetime.utcnow().timetuple())}}
            }
        response = requests.post(URL + 'chats.json', data=json.dumps(payload))
        logging.debug(str(response))
        new_chat = json.loads(response.text)
        chat_id = new_chat['name']
        logging.debug(str(chat_id))
        logging.debug(str(post_data["_id"]["facebookId"]))
        logging.debug(str(facebook_id_comprador))
        FirebaseCommunication.__newUserChat(facebook_id_comprador, chat_id)
        FirebaseCommunication.__newUserChat(post_data["_id"]["facebookId"], chat_id)

import json
import datetime
import time
import os
import requests

from server.logger import Logger

URL = 'https://melli-7552.firebaseio.com/'

LOGGER = Logger.get(__name__)

FIREBASE_KEY = os.environ.get('FIREBASE_KEY')


class FirebaseCommunication:

    @staticmethod
    def __new_user_chat(facebook_id, chat_key):
        user = requests.get(URL + 'userChats/' + facebook_id + '.json')
        if user.text == "null":
            dict = {'chats': []}
            requests.put(URL + 'userChats/' + facebook_id + '.json', data=json.dumps(dict))
        chats = requests.get(URL + 'userChats/' + facebook_id + '/chats.json')
        if chats.text != "null":
            new_chat_list = json.loads(chats.text)
            new_chat_list.append(chat_key)
            LOGGER.debug("Se ha credo un nuevo chat: " + str(new_chat_list))
        else:
            new_chat_list = [chat_key]
        requests.put((URL + 'userChats/' + facebook_id + '.json'), data=json.dumps({'chats': new_chat_list}))

    @staticmethod
    def __new_user(data):
        facebook_id = data['facebookId']
        data.pop('facebookId')
        json_data = {
                facebook_id: data
            }
        requests.put(URL + 'user/' + facebook_id + '.json', data=json.dumps(json_data))

    @staticmethod
    def new_chat(facebook_id_comprador, post_data):
        payload = {
                "picture": post_data["pictures"],
                "title": post_data["title"],
                "publicationId": post_data["ID"],
                "messages": {"0":{"senderId": post_data["_id"]["facebookId"],
                                  "text": "Gracias por su compra!",
                                  "timestamp": time.mktime(datetime.datetime.utcnow().timetuple())}}
            }
        response = requests.post(URL + 'chats.json', data=json.dumps(payload))
        new_chat = json.loads(response.text)
        chat_id = new_chat['name']
        FirebaseCommunication.__new_user_chat(facebook_id_comprador, chat_id)
        FirebaseCommunication.__new_user_chat(post_data["_id"]["facebookId"], chat_id)

    @staticmethod
    def send_notification(facebook_id, title, body):
        try:
            url = 'https://fcm.googleapis.com/fcm/send'
            json_data = {
                "to": "/topics/allDevices",
                "notification": {
                    "content_available": True,
                    "title": title,
                    "body": body
                },
                "data": {
                    "user_id": facebook_id,
                    "content_available": True,
                    "title": title,
                    "body": body
                }
            }

            response = requests.post(url, json=json_data, headers={'Authorization': "key=" + FIREBASE_KEY,
                                                                   'Content-type': 'application/json'})
            LOGGER.info('Mensaje enviado satisfactoriamente. Respuesta: ' + response.text)
        except Exception as e:
            LOGGER.error('Surgio un problema al enviar el mensaje: ' + str(e))
            LOGGER.error('Respuesta: ' + response.text)

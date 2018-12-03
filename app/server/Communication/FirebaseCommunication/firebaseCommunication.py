import json
import datetime
import time
import os
import requests
URL = 'https://melli-7552.firebaseio.com/'
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

URL = 'https://fcm.googleapis.com/project/melli-7552//send'
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
            logging.debug(str(new_chat_list))
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
    def send_notification(title, categoria, facebook_id):
        try:
            json_data = {
                'id': facebook_id,
                'categoria': categoria,
                'title': title
            }

            response = requests.post(URL, json=json_data, headers={'Authorization': FIREBASE_KEY,
                                                                   'Content-type': 'application/json'})
            logging.info('Mensaje enviado satisfactoriamente. Respuesta: ' + response.json())
        except Exception as e:
            logging.error('Surgio un problema al enviar el mensaje: ' + str(e))

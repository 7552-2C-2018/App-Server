import requests
import json

class FacebookCommunication:
    def __init__(self):
        pass

    @staticmethod
    def ValidateUser(facebook_id, token):
        url = 'https://graph.facebook.com/me?access_token=' + token
        facebook_response = requests.get(url)
        facebook_payload = json.loads(facebook_response.text)
        return facebook_response.status_code == 200 and facebook_payload['id'] == facebook_id

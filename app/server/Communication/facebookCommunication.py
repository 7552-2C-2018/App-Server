import requests


class FacebookCommunication:
    def __init__(self):
        pass

    @staticmethod
    def ValidateUser(token):
        url = 'https://graph.facebook.com/me?access_token=' + token
        facebook_response = requests.get(url)
        return facebook_response

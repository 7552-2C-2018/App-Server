from server.setup import app
import logging
import json
import datetime
import time
from bson import json_util, ObjectId
logging.basicConfig(filename='debug.log', level=logging.DEBUG)
with app.app_context():
    workingCollection = app.database.posts


class PostTransactions:

    def __init__(self):
        pass



    @staticmethod
    def __parseData(data):
        parsed_data = {}
        if "title" in data.keys():
            parsed_data["title"] = data["title"]
        if "desc" in data.keys():
            parsed_data["description"] = data["desc"]
        if "stock" in data.keys():
            parsed_data["stock"] = data["stock"]
        if "payments" in data.keys():
            parsed_data["payments"] = data["payments"]
        if "price" in data.keys():
            parsed_data["price"] = data["price"]
        if "new" in data.keys():
            parsed_data["new"] = data["new"]
        if "category" in data.keys():
            parsed_data["category"] = data["category"]
        if "pictures" in data.keys():
            parsed_data["pictures"] = data["pictures"]
        if "shipping" in data.keys():
            parsed_data["shipping"] = data["shipping"]
        if "latitude" in data.keys() and "longitude" in data.keys():
            parsed_data["coordenates"] = [data["latitude"], data["longitude"]]
        return parsed_data

    @staticmethod
    def findPostById(user_id, publ_date):
        return workingCollection.find_one({'_id': {"facebookId": user_id, "publication_date": publ_date}})

    @staticmethod
    def getPosts():
        response = list(workingCollection.find({}, {"title": 1, "price": 1, 'pictures': {'$slice': 1}, "payments": 1}))
        return response

    @staticmethod
    def newPost(data):
        parsed_data = PostTransactions.__parseData(data)
        publ_date = time.mktime(datetime.datetime.utcnow().timetuple())
        id = workingCollection.insert_one({"_id": {"facebookId": data['facebookId'], "publication_date": publ_date}})
        workingCollection.update_one({"_id": {"facebookId":  data['facebookId'], "publication_date": publ_date}},
                                     {'$set': parsed_data})
        return id

    @staticmethod
    def updatePostData(data):
        parsed_data = PostTransactions.__parseData(data)
        if parsed_data:
            workingCollection.update_one({'_id': {"facebookId": data['facebookId'],
                                                  "publication_date": int(data['publDate'])}}, {'$set': parsed_data})

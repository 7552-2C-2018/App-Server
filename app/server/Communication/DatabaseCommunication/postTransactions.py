from server.setup import app
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)
with app.app_context():
    workingCollection = app.database.posts


class PostTransactions:

    def __init__(self):
        pass

    @staticmethod
    def __parseUpdateData(data):
        parsed_data = {}
        if "title" in data.keys():
            parsed_data["title"] = data["title"]
        if "description" in data.keys():
            parsed_data["description"] = data["desc"]
        if "stock" in data.keys():
            parsed_data["stock"] = data["stock"]
        if "payments" in data.keys():
            parsed_data["payments"] = data["payments"]
        if "email" in data.keys():
            parsed_data["email"] = data["email"]
        return parsed_data

    @staticmethod
    def findPostById(post_id):
        return workingCollection.find_one({'_id': post_id})

    @staticmethod
    def getPosts():
        return workingCollection.find()

    @staticmethod
    def newPost(user_id, title, desc, stock, payments, email):
        id = workingCollection.insert_one({"facebookId": user_id,
                                           "title": title,
                                           "description": desc,
                                           "stock": stock,
                                           "payments": payments,
                                           "email": email})
        return id

    @staticmethod
    def updatePostrData(data):
        parsed_data = PostTransactions.__parseUpdateData(data)
        if parsed_data:
            workingCollection.update_one({'_id': data['post_id']}, {'$set': parsed_data})

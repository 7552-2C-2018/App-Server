from server.setup import app
import logging
import json
import datetime
import time

logging.basicConfig(filename='debug.log', level=logging.DEBUG)
with app.app_context():
    workingCollection = app.database.posts


class PostTransactions:

    def __init__(self):
        pass

    @staticmethod
    def __validate_estado(estado):
        return estado in ["activo", "pausado", "cancelado"]

    @staticmethod
    def __parse_data(data):
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
    def find_post_by_post_id(post_id):
        logging.debug(post_id)
        return workingCollection.find_one({'ID': post_id}, {"_id": 1, "ID": 1, "title": 1, 'pictures': {'$slice': 1}})


    @staticmethod
    def getPosts():
        response = list(workingCollection.find({},
                                               {"_id": 0, "ID": 1, "title": 1, "price": 1, 'pictures': {'$slice': 1}}))
        return response

    @staticmethod
    def new_post(data):
        parsed_data = PostTransactions.__parse_data(data)
        publ_date = time.mktime(datetime.datetime.utcnow().timetuple())
        post_id = data['facebookId'] + str(int(publ_date))
        parsed_data["ID"] = post_id
        parsed_data["estado"] = "activo"
        workingCollection.insert_one({"_id": {"facebookId": data['facebookId'], "publication_date": publ_date}})
        workingCollection.update_one({"_id": {"facebookId": data['facebookId'], "publication_date": publ_date}},
                                     {'$set': parsed_data})
        return post_id

    @staticmethod
    def find_post_by_user_id(user_id):
        return list(workingCollection.find({"_id.facebookId": user_id},
                                           {"_id": 0, "ID": 1, "title": 1, "price": 1, 'pictures': {'$slice': 1}}))

    @staticmethod
    def update_post_data(data):
        # parsed_data = PostTransactions.__parseData(data)
        estado_valido = PostTransactions.__validate_estado(data["estado"])
        if estado_valido:
            return workingCollection.update_one({'ID': data['postId']}, {'$set': {"estado": data["estado"]}})
        else:
            return "estado Invalido"

from server.setup import app
import logging
import json
import datetime
import time
import pymongo
import base64
import qrcode
from io import BytesIO
import re
from bson.son import SON

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
        if data["title"] is not None:
            parsed_data["title"] = data["title"]
        if data["desc"] is not None:
            parsed_data["description"] = data["desc"]
        if data["stock"] is not None:
            parsed_data["stock"] = data["stock"]
        if data["payments"] is not None:
            parsed_data["payments"] = data["payments"]
        if data["price"] is not None:
            parsed_data["price"] = data["price"]
        if data["new"] is not None:
            parsed_data["new"] = data["new"]
        if data["category"] is not None:
            parsed_data["category"] = data["category"]
        if data["pictures"] is not None:
            parsed_data["pictures"] = data["pictures"]
        if data["shipping"] is not None:
            parsed_data["shipping"] = data["shipping"]
        if data["street"] is not None:
            parsed_data["street"] = data["street"]
        if data["latitude"] is not None and data["longitude"]:
            parsed_data["coordenates"] = [data["longitude"], data["latitude"]]
        return parsed_data

    @staticmethod
    def find_post_by_post_id(post_id):
        logging.debug(post_id)
        return workingCollection.find_one({'ID': post_id})


    @staticmethod
    def getPosts(data):
        queryFilters = PostTransactions.__build_query_filters(data)
        pipeline = [
            {
                u"$project": {
                    u"_id": 0,
                    u"posts": u"$$ROOT"
                }
            },
            {
                u"$lookup": {
                    u"localField": u"posts._id.facebookId",
                    u"from": u"users",
                    u"foreignField": u"facebookId",
                    u"as": u"users"
                }
            },
            {
                u"$unwind": {
                    u"path": u"$users",
                    u"preserveNullAndEmptyArrays": False
                }
            },
            {
                u"$match":
                    queryFilters

            },
            {
                u"$project": {
                    u"price": u"$posts.price",
                    u"ID": u"$posts.ID",
                    u"title": u"$posts.title",
                    u"coordenates": u"$posts.coordenates",
                    'pictures': {"$slice": ["$posts.pictures", 0, 1]},
                    u'totalPoints': u"$users.totalPoints"
                }

            },
            {
                u"$sort": SON([(u"users.totalPoints", -1)])
            }
        ]

        cursor = workingCollection.aggregate(
            pipeline,
            allowDiskUse=True
        )
        # response = list(workingCollection.find(queryFilters,
        #                                        {"_id": 0, "ID": 1, "title": 1, "price": 1,
        #                                         "coordenates": 1, 'pictures': {'$slice': 1}}
        #                                       ))
        return list(cursor)

    @staticmethod
    def new_post(data):
        parsed_data = PostTransactions.__parse_data(data)
        publ_date = time.mktime(datetime.datetime.utcnow().timetuple())
        post_id = data['facebookId'] + str(int(publ_date))
        parsed_data["ID"] = post_id
        parsed_data["estado"] = "activo"
        parsed_data["qr"] = PostTransactions.__generate_qr(post_id)
        workingCollection.insert_one({"_id": {"facebookId": data['facebookId'], "publication_date": publ_date}})
        workingCollection.update_one({"_id": {"facebookId": data['facebookId'], "publication_date": publ_date}},
                                     {'$set': parsed_data})
        return post_id

    @staticmethod
    def find_post_by_user_id(user_id):
        return list(workingCollection.find({"_id.facebookId": user_id},
                                           {"_id": 0, "ID": 1, "title": 1
                                               , "price": 1, 'pictures': {'$slice': 1}}))

    @staticmethod
    def update_post_data(data):
        parsed_data = PostTransactions.__parse_data(data)
        estado_valido = PostTransactions.__validate_estado(data["estado"])
        if estado_valido or "estado" not in parsed_data.keys():
            return workingCollection.update_one({'ID': data['postId']}, {'$set': {"estado": data["estado"]}})
        else:
            return None

    @staticmethod
    def __build_query_filters(data):
        filters = {}
        if data['distancia'] is not None and data['latitud'] is not None and data['longitud'] is not None:
            filters["posts.coordenates"] = {}
            filters["posts.coordenates"]["$geoWithin"] = {}
            filters["posts.coordenates"]["$geoWithin"]["$center"] = [[data['longitud'], data['latitud']], data['distancia']]

        if data['precioMinimo'] is not None or data['precioMaximo'] is not None:
            filters["posts.price"] = {}
        if data['precioMaximo'] is not None:
            filters['posts.price']['$lte'] = data['precioMaximo']
        if data['precioMinimo'] is not None:
            filters['posts.price']['$gte'] = data['precioMinimo']
        if data['estado'] is not None:
            if data['estado'] == "nuevo":
                filters['posts.new'] = True
            else:
                filters['posts.new'] = False
        if data['envio'] is not None:
            if data["envio"] == 1:
                filters['posts.shipping'] = True
            if data["envio"] == 0:
                filters['posts.shipping'] = False
        if data['categoria'] is not None:
            filters['posts.category'] = re.compile(data['categoria'], re.IGNORECASE)
        if data['search'] is not None:
            filters['posts.title'] = {}

            filters['posts.title']["$regex"] = re.compile(data['search'], re.IGNORECASE)
        return filters

    @staticmethod
    def __generate_qr( post_id):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(post_id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return str(base64.b64encode(buffered.getvalue()))

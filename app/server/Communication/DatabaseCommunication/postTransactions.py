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
        if "title" in  data.keys() and data["title"] is not None:
            parsed_data["title"] = data["title"]
        if "desc" in  data.keys() and data["desc"] is not None:
            parsed_data["description"] = data["desc"]
        if "stock" in  data.keys() and data["stock"] is not None:
            parsed_data["stock"] = data["stock"]
        if "payments" in  data.keys() and data["payments"] is not None:
            parsed_data["payments"] = data["payments"]
        if "price" in  data.keys() and data["price"] is not None:
            parsed_data["price"] = data["price"]
        if "new" in  data.keys() and data["new"] is not None:
            parsed_data["new"] = data["new"]
        if "category" in  data.keys() and data["category"] is not None:
            parsed_data["category"] = data["category"]
        if "pictures" in  data.keys() and data["pictures"] is not None:
            parsed_data["pictures"] = data["pictures"]
        if "shipping" in  data.keys() and data["shipping"] is not None:
            parsed_data["shipping"] = data["shipping"]
        if "street" in  data.keys() and data["street"] is not None:
            parsed_data["street"] = data["street"]
        if "latitude" in  data.keys() and data["latitude"] is not None and \
                "longitude" in  data.keys() and data["longitude"]:
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
        if 'distancia' in data.keys() and 'latitud' in data.keys() and 'longitud' in data.keys():
            if data['distancia'] is not None and data['latitud'] is not None and data['longitud'] is not None:
                filters["posts.coordenates"] = {}
                filters["posts.coordenates"]["$geoWithin"] = {}
                filters["posts.coordenates"]["$geoWithin"]["$center"] = [[data['longitud'], data['latitud']], data['distancia']]
        if ('precioMinimo' in data.keys() and data['precioMinimo'] is not None) or \
                ('precioMaximo' in data.keys() and data['precioMaximo'] is not None):
                filters["posts.price"] = {}
        if 'precioMaximo' in data.keys():
            if data['precioMaximo'] is not None:
                filters['posts.price']['$lte'] = data['precioMaximo']
        if 'precioMaximo' in data.keys():
            if data['precioMinimo'] is not None:
                filters['posts.price']['$gte'] = data['precioMinimo']
        if 'estado' in data.keys():
            if data['estado'] is not None:
                if data['estado'] == "nuevo":
                    filters['posts.new'] = True
                else:
                    filters['posts.new'] = False
        if 'envio' in data.keys():
            if data['envio'] is not None:
                if data["envio"] == 1:
                    filters['posts.shipping'] = True
                if data["envio"] == 0:
                    filters['posts.shipping'] = False
        if 'categoria' in data.keys():
            if data['categoria'] is not None:
                filters['posts.category'] = re.compile(data['categoria'], re.IGNORECASE)
        if 'search' in data.keys():
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

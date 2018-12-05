from server.setup import app
import logging
import datetime
import time
import pymongo

logging.basicConfig(filename='debug.log', level=logging.DEBUG)
with app.app_context():
    questions_collection = app.database.questions


class QuestionTransactions:

    def __init__(self):
        pass
    
    @staticmethod
    def findQuestion(question_id):
        return questions_collection.find_one({'ID': question_id})


    @staticmethod
    def getQuestions(postId):
        return  list(questions_collection.find({"_id.postId": postId})
                     .sort("_id.publication_date", pymongo.DESCENDING))

    @staticmethod
    def newQuestion(data):
        parsed_data = {}
        publ_date = time.mktime(datetime.datetime.utcnow().timetuple())
        question_id = data['postId'] + str(int(publ_date))
        parsed_data["ID"] = question_id
        parsed_data["userId"] = data["facebookId"]
        parsed_data["pregunta"] = data["question"]
        questions_collection.insert_one({"_id": {"postId": data['postId'], "publication_date": publ_date}})
        questions_collection.update_one({"_id": {"postId": data['postId'], "publication_date": publ_date}},
                                     {'$set': parsed_data})
        return question_id


    @staticmethod
    def updateQuestion(data):
        date_now = time.mktime(datetime.datetime.utcnow().timetuple())
        questions_collection.update_one({'ID': data['questionId']}, {'$set': {"answer": data["respuesta"],
                                                                              "answer_date": date_now}})
        logging.debug(questions_collection.find_one({'ID': data['questionId']}))
        return questions_collection.find_one({'ID': data['questionId']})

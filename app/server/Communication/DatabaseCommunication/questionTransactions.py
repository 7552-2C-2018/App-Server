from server.setup import app
import logging
import datetime
import time
import pymongo

logging.basicConfig(filename='debug.log', level=logging.DEBUG)
with app.app_context():
    workingCollection = app.database.questions


class QuestionTransactions:

    def __init__(self):
        pass
    
    @staticmethod
    def findQuestion(question_id):
        return workingCollection.find_one({'ID': question_id})


    @staticmethod
    def getQuestions():
        response = list(workingCollection.find().sort("_id.publication_date", pymongo.DESCENDING))
        return response

    @staticmethod
    def newQuestion(data):
        parsed_data = {}
        publ_date = time.mktime(datetime.datetime.utcnow().timetuple())
        question_id = data['postId'] + str(int(publ_date))
        parsed_data["ID"] = question_id
        parsed_data["userId"] = data["facebookId"]
        workingCollection.insert_one({"_id": {"postId": data['postId'], "publication_date": publ_date}})
        workingCollection.update_one({"_id": {"postId": data['postId'], "publication_date": publ_date}},
                                     {'$set': parsed_data})
        return question_id


    @staticmethod
    def updateQuestion(data):
        return workingCollection.update_one({'ID': data['questionId']}, {'$set': {"answer": data["respuesta"]}})

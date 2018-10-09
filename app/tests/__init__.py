import os
os.environ.setdefault('MONGO_URL', 'mongodb://127.0.0.1:27017/test')
import unittest
from server.setup import app


class GenericTest(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        try:
            database.users.drop()
        except Exception:
            pass


def tearDown(self):
        self.app_context.pop()


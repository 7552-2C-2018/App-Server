import os
os.environ.setdefault('MONGO_URL', 'mongodb://127.0.0.1:27017/testDatabase')
import unittest
from server.setup import app


class GenericTest(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        try:
            app.database.users.drop()
        except Exception:
            pass
            app.database.create_collection('users')
        try:
            app.database.posts.drop()
        except Exception:
            pass
        app.database.create_collection('posts')

def tearDown(self):
        self.app_context.pop()


from server.setup import app
from flask import Flask
from . import GenericTest


class TestMock(GenericTest):

    def test_mock(self):
        assert 1 == 1

    def test_db(self):
        assert app.database.prueba.find() is not None

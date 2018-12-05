import time

from server.setup import app

from server.services.Monitoring.monitor import monitor
from . import GenericTest


class TestFunctions(GenericTest):

    def test_mock(self):
        assert 1 == 1

    def test_db(self):
        assert app.database.prueba.find() is not None

    def test_monitoring(self):
        monitor(time.time(), time.time(), "un/path/de/prueba", "get")
        assert len(list(app.database.stats.find())) != 0

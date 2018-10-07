from server.setup import app
from flask import Flask

with app.app_context():
    db = app.database
def test_mock():
	assert 1==1

def test_db():
	assert db.prueba.find() is not None
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import pytest
from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_signup(client):
    response = client.post("/user/signup", data={
        "username": "Max",
        "password": "MyPassword"
    })
    assert response.status_code == 200

def test_login(client):
    response = client.post("/user/login", data={
        "username": "Max",
        "password": "MyPassword"
    })
    assert response.status_code == 200

    response = client.post("/user/login", data={
        "username": "Max",
        "password": "Incorrect"
    })
    assert response.status_code == 400

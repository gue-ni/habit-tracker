import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import pytest
from app import create_app, db


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    app.config["WTF_CSRF_ENABLED"] = False

    # other setup can go here
    db.create_db()

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200

    response = client.get("/about")
    assert response.status_code == 200


def test_signup(client):
    response = client.post(
        "/user/signup",
        data={
            "username": "Max",
            "password": "MyPassword",
            "confirm_password": "MyPassword",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_login_unknown_user(client):
    response = client.post(
        "/user/login",
        data={"username": "DoesNotExist", "password": "MyPassword"},
        follow_redirects=True,
    )
    assert response.status_code == 404


def test_login_invalid_password(client):
    response = client.post(
        "/user/login",
        data={"username": "Max", "password": "WrongPassword"},
        follow_redirects=True,
    )
    assert response.status_code == 400


def test_login_valid_password(client):
    response = client.post(
        "/user/login",
        data={"username": "Max", "password": "MyPassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/dashboard"

    response = client.get("/user/logout", follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/"

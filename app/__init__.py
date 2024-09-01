from flask import Flask
from flask_login import LoginManager
import os

import app.db as db
from app.models import User


def create_app(config_class=None):
    app = Flask(__name__)

    secret_key = os.getenv("SECRET_KEY", "change-this")
    app.config["SECRET_KEY"] = secret_key

    print(f"SECRET_KEY={secret_key}")

    login_manager = LoginManager()
    login_manager.login_view = "user.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user = db.get_user_by_id(user_id)
        if not user:
            return None
        else:
            (id, name, hash) = user
            return User(str(id), name)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.user import bp as user_bp

    app.register_blueprint(user_bp, url_prefix="/user")

    from app.event import bp as event_bp

    app.register_blueprint(event_bp, url_prefix="/event")

    @app.route("/test/")
    def test_page():
        return "<h1>Testing the Flask Application Factory Pattern</h1>"

    return app

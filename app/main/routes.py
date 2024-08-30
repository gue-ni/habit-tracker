from flask import render_template
from app.main import bp
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/dashboard")
def dashboard():
    print(current_user.name)
    return render_template("index.html")



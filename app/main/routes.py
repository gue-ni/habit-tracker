from flask import render_template
from app.main import bp
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
)


import app.db as db


@bp.route("/")
def index():
    return render_template("index.html")


# @bp.route("/dashboard")
# def dashboard():
#    print(current_user.name)
#    return render_template("index.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    events = db.get_all_events_by_owner(current_user.id)
    return render_template(
        "dashboard.html", user=current_user, events_todo=events, events_done=events
    )

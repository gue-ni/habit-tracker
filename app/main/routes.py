from flask import render_template, redirect, url_for
from flask_login import login_required, current_user


from app.main import bp
from app import db
from app.utils import get_todos, compute_all_streaks


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@bp.route("/about")
def about():
    return render_template("index.html")


@bp.route("/dashboard")
@login_required
def dashboard():

    compute_all_streaks(current_user.id)

    events = db.get_all_events(current_user.id)

    todo = get_todos(current_user.id)

    return render_template(
        "dashboard.html", user=current_user, events_todo=todo, all_events=events
    )

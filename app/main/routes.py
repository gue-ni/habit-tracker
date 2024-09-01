from flask import render_template, redirect, url_for
from app.main import bp
from flask_login import (
    login_required,
    current_user,
)


import app.db as db


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
    all_events = db.get_all_events_by_owner(current_user.id)
    print(f"events={all_events}")

    # check streak

    # todo
    todo = []
    todo_daily = db.get_todo_daily_events(current_user.id)
    todo += todo_daily

    todo_week = db.get_todo_repeat_events(current_user.id)
    todo += todo_week

    print(f"todo_daily={todo_daily}")
    print(f"todo_week={todo_week}")

    return render_template(
        "dashboard.html", user=current_user, events_todo=todo, all_events=all_events
    )

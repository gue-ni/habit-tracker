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
    all_events = db.get_all_events(current_user.id)
    # print(f"events={all_events}")

    # check streaks
    # TODO: in the future, this should only recalculate if the streak is active if a datestamp
    for event in all_events:
        event_id = event[0]
        event_name = event[1]
        event_type = event[5]
        streak = event[7]

        if streak != None and streak > 1:
            date_since = None
            if event_type == "DAILY":
                date_since = db.get_yesterday()
                occurances = db.get_all_occurances_between(
                    event_id=event_id, start_date=date_since, end_date=db.get_today()
                )

                print(event_name, occurances)

                if len(occurances) == 0:
                    print(f"streak for event {event_name} should be reset")
                    #db.delete_streak(event_id=event_id)
                else:
                    print(f"streak for event {event_name} is still active")

            else:
                date_since = db.get_yesterday()
                occurances = db.get_all_occurances_between(
                    event_id=event_id, start_date=date_since, end_date=db.get_today()
                )
                print(event_name, occurances)

                if len(occurances) < 3:
                    # db.update_streak(event_id=event_id, streak=0)
                    print(f"reset streak for event {event_name}")
                    pass

    all_events = db.get_all_events(current_user.id)

    test = db.get_day_streak(event_id=9)
    print(test)

    # todo
    todo = []
    todo_daily = db.get_todo_daily_events(current_user.id)
    todo += todo_daily

    todo_week = db.get_todo_repeat_events(current_user.id)
    todo += todo_week

    # print(f"todo_daily={todo_daily}")
    # print(f"todo_week={todo_week}")

    return render_template(
        "dashboard.html", user=current_user, events_todo=todo, all_events=all_events
    )

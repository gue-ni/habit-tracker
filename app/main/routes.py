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


def get_todos(user_id):
    todo = []
    todo_daily = db.get_todo_daily_events(user_id)
    todo += todo_daily

    todo_week = db.get_todo_repeat_events(user_id)
    todo += todo_week
    return todo

# this should also be called after recording an occurence
def compute_streak(event_id):
    event = db.get_event(event_id)
    repeat = event[5] # TODO: this might not be correct
    occurences = db.get_all_occurences(event_id=event_id)
    occurences.reverse()

    streak = 0

    if repeat == 'DAILY':
        for i in range(len(occurences) - 1):
        current_date = date(occurences[i][1]) 
        previous_date = date(occurences[i + 1][1])

        difference = current_date - previous_date
        if difference.days == 1:
            streak = streak + 1
        else:
            break

    else:
        repeat_per_week = event[5] # might not be correct
        # streak = count_current_week + the count of the weeks where at least rpw was achieved
        pass

  return streak


# should this be moved to event?
@bp.route("/dashboard")
@login_required
def dashboard():

    streak_to_recompute = db.get_all_streaks_for_user(current_user.id)
    print(f"recompute={streak_to_recompute}")
    for streak in streak_to_recompute:
      event_id = streak[0]
      old_count = streak[2]
      new_count = compute_steak(event_id=event_id)
      db.update_streak(event_id=event_id, streak=new_count)

    all_events = db.get_all_events(current_user.id)
    print(f"all_events={all_events}")

    todo = get_todos(current_user.id)
    print(f"todo={todo}")

    return render_template(
        "dashboard.html", user=current_user, events_todo=todo, all_events=all_events
    )

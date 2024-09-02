from collections import defaultdict
from datetime import date, datetime


from flask import render_template, redirect, url_for, current_app
from flask_login import login_required, current_user


from app.main import bp
from app import db
#import app.db as db


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

    todo_week = db.get_todo_weekly_events(user_id)
    #print(f"weekly={todo_week}")
    todo += todo_week
    return todo

# this should also be called after recording an occurence
def compute_streak(event_id):
    event = db.get_event(event_id)
    repeat = event[5] # TODO: this might not be correct

    occurences = db.get_all_occurences(event_id=event_id)
    occurences.reverse()

    if len(occurences) == 0:
        return 0


    today = datetime.now().date()

    dates = [datetime.strptime(occurence[1], "%Y-%m-%d").date() for occurence in occurences]


    if len(dates) == 1 and dates[0] == today:
        return 1

    streak = 1

    if repeat == 'DAILY':
        for i in range(len(dates) - 1):

            current_date = dates[i]
            previous_date = dates[i+1]

            difference = current_date - previous_date
            if difference.days == 1:
                streak = streak + 1
            else:
                break
    else:
        repeat_per_week = event[7]

        event_counts = defaultdict(int)

        for date in dates:
            year, week, _ = date.isocalendar()
            event_counts[(year, week)] += 1

        current_year, current_week, _ = datetime.now().isocalendar()

        year, week = current_year, current_week

        while (year, week) in event_counts:
            if int(repeat_per_week) <= event_counts[(year, week)]:
                streak = streak + 1
            else:
                break

            week -= 1
            if week == 0:
                year -= 1
                week = 52

    return streak


@bp.route("/dashboard")
@login_required
def dashboard():
    streak_to_recompute = db.get_all_streaks_for_user(current_user.id)

    for streak in streak_to_recompute:
      event_id = streak[0]
      old_count = streak[2]
      new_count = compute_streak(event_id=event_id)
      #print(f"{streak}, old_count={old_count}, new_count={new_count}")
      #db.update_streak(event_id=event_id, streak=new_count)

    all_events = db.get_all_events(current_user.id)
    #print(f"all_events={all_events}")

    todo = get_todos(current_user.id)
    print(f"todo={todo}")

    return render_template(
        "dashboard.html", user=current_user, events_todo=todo, all_events=all_events
    )

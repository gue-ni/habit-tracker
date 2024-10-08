from collections import defaultdict
import datetime


from flask import render_template, redirect, url_for
from flask_login import login_required, current_user


from app.main import bp
from app import db
from app.models import User, AppException
from app.utils import get_current_date


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

    todo_week = db.get_todo_weekly_events(user_id, get_current_date())
    todo += todo_week

    return todo


def compute_daily_streak(dates, current_date):
    pass


def compute_quit_streak(dates, current_date):
    pass


def compute_weekly_streak(dates, current_date, target_weekly_repeat):
    pass


def previous_week(year, week):
    week -= 1
    if week == 0:
        year -= 1
        week = 52

    return (year, week)


def compute_streak(event_id):
    event = db.get_event(event_id)
    # print(f"compute_streak {event[1]}")
    repeat = event[5]

    occurences = db.get_all_occurences(event_id=event_id)
    occurences.reverse()

    today = datetime.datetime.now().date()

    dates = [
        datetime.datetime.strptime(occurence[1], "%Y-%m-%d").date()
        for occurence in occurences
    ]

    if len(dates) == 0:
        return 0

    if len(dates) == 1 and dates[0] == today:
        return 1

    streak = 0

    if repeat == "DAILY":

        yesterday = today - datetime.timedelta(days=1)

        # print(f"today={today}, yesterday={yesterday}")
        # print(dates)

        if not (dates[0] == today or dates[0] == yesterday):
            # print("early return")
            streak = 0
            return streak

        streak = 1

        for i in range(len(dates) - 1):
            current_date = dates[i]
            previous_date = dates[i + 1]
            difference = current_date - previous_date

            # print("for loop", current_date, previous_date, difference)

            if difference.days == 1:
                streak = streak + 1
            else:
                break

    else:
        count_target = event[7]

        event_counts = defaultdict(int)

        # count occurences per week
        for date in dates:
            year, week, _ = date.isocalendar()
            event_counts[(year, week)] += 1

        current_year, current_week, _ = datetime.datetime.now().isocalendar()
        year, week = current_year, current_week

        # streak can still be valid if last event was last week
        if not (year, week) in event_counts:
            (year, week) = previous_week(year, week)

        while (year, week) in event_counts:

            count = event_counts[(year, week)]

            # streak counts if target was met or week is not yet finished
            if count >= count_target or week == current_week:
                streak += count

            (year, week) = previous_week(year, week)

    return streak


def compute_all_streaks(user_id):
    streak_to_recompute = db.get_all_streaks_for_user(user_id)

    for streak in streak_to_recompute:
        event_id = streak[0]
        old_count = streak[2]
        new_count = compute_streak(event_id=event_id)
        db.update_streak(event_id=event_id, streak=new_count)


@bp.route("/dashboard")
@login_required
def dashboard():

    compute_all_streaks(current_user.id)

    events = db.get_all_events(current_user.id)

    todos = get_todos(current_user.id)

    return render_template(
        "dashboard.html", user=current_user, events_todo=todos, all_events=events
    )

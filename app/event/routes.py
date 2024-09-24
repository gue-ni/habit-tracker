from app import db
from app.event import bp
from app.utils import datestring_to_obj, obj_to_datestring, get_current_date


import random
from datetime import datetime, timedelta, date
from enum import Enum


from flask import render_template, request, url_for, redirect, abort, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, EqualTo


class EventType(Enum):
    HABIT = "HABIT"
    QUIT = "QUIT"
    MEASURE = "MEASURE"


class EventFrequency(Enum):
    DAILY = "DAILY"
    ONE_PER_WEEK = "1_PER_WEEK"
    TWO_PER_WEEK = "2_PER_WEEK"
    THREE_PER_WEEK = "3_PER_WEEK"
    FOUR_PER_WEEK = "4_PER_WEEK"
    FIVE_PER_WEEK = "5_PER_WEEK"


class CreateEventForm(FlaskForm):
    event_name = StringField("Name", validators=[DataRequired()])
    event_emoji = SelectField(
        "Emoji",
        choices=[
            "💪🏼",
            "🏃‍♂️",
            "️⚽",
            "🏋️‍♀️",
            "😴",
            "🛌",
            "🌙",
            "🎓",
            "🧠",
            "📚",
            "📖",
            "💧",
        ],
        validators=[DataRequired()],
    )
    event_description = StringField("Description")
    event_type = SelectField(
        "Type",
        choices=[(e.name, e.value) for e in EventType],
        validators=[DataRequired()],
    )
    event_repeat = SelectField(
        "Repeat",
        choices=[e.value for e in EventFrequency],
        validators=[DataRequired()],
    )
    submit = SubmitField("Create")


class RecordEventForm(FlaskForm):
    numeric_value = DecimalField("Numeric Value")
    submit = SubmitField("Done")


def get_last_five_weeks_dates():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())

    days = []

    for i in range(5):
        week_start = start_of_week - timedelta(weeks=i)
        week_dates = [week_start + timedelta(days=d) for d in range(7)]
        week_dates.reverse()
        days += week_dates

    return [day.date() for day in days]


@bp.route("/<int:id>/numeric")
def numeric(id):
    return db.get_all_measurements(id)


@bp.route("/<int:id>", methods=["GET"])
def event(id):
    event = db.get_event_by_id(event_id=id, user_id=current_user.id)
    if not event:
        abort(404)

    streak = db.get_streak(event_id=id)

    occurences = db.get_all_occurences_of_event(event_id=id)
    occurences = [datestring_to_obj(occurence[1]) for occurence in occurences]

    last_five_weeks = get_last_five_weeks_dates()

    today = date.today()

    calendar = [
        (day.strftime("%d"), day in occurences, obj_to_datestring(day), day <= today)
        for day in last_five_weeks
    ]
    calendar.reverse()

    return render_template(
        "event.html",
        event=event,
        streak=streak,
        calendar=calendar,
        current_date=get_current_date(),
    )


def random_hex_color():
    while True:
        (r, g, b) = (
            random.randint(0, 150),
            random.randint(0, 150),
            random.randint(0, 150),
        )

        hex_color = f"#{r:02x}{g:02x}{b:02x}"

        # check if color is dark enough
        brightness = 0.299 * r + 0.587 * g + 0.114 * b
        if brightness < 120:
            return hex_color


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new_event():
    form = CreateEventForm()

    if request.method == "POST":
        event_name = form.event_name.data
        event_type = form.event_type.data
        event_emoji = form.event_emoji.data
        event_repeat = form.event_repeat.data
        event_description = form.event_description.data

        event_repeat_per_week = None

        if event_repeat != "DAILY":
            if event_repeat == EventFrequency.ONE_PER_WEEK.value:
                event_repeat_per_week = 1
            elif event_repeat == EventFrequency.TWO_PER_WEEK.value:
                event_repeat_per_week = 2
            elif event_repeat == EventFrequency.THREE_PER_WEEK.value:
                event_repeat_per_week = 3
            elif event_repeat == EventFrequency.FOUR_PER_WEEK.value:
                event_repeat_per_week = 4
            elif event_repeat == EventFrequency.FIVE_PER_WEEK.value:
                event_repeat_per_week = 5

            event_repeat = "WEEKLY"

        print(event_repeat, event_repeat_per_week)

        hex_color = random_hex_color()

        ok = db.insert_event(
            event_name=event_name,
            owner=current_user.id,
            event_type=event_type,
            event_repeat=event_repeat,
            event_emoji=event_emoji,
            event_color=hex_color,
            event_description=event_description,
            event_repeat_per_week=event_repeat_per_week,
        )

        if not ok:
            abort(500)

        return redirect(url_for("main.dashboard"))

    else:
        return render_template("new_event.html", form=form)


@bp.route("/<int:id>/record", methods=["GET", "POST"])
@login_required
def record_event(id):
    current_date = get_current_date()
    date = request.args.get("date", current_date)
    form = RecordEventForm()

    if request.method == "POST":
        numeric_value = form.numeric_value.data

        ok = False

        if numeric_value:
            numeric_value = float(numeric_value)
            ok = db.insert_measurement_of_event(
                event_id=id, value=numeric_value, date=date
            )
        else:
            ok = db.insert_occurence_of_event(event_id=id, date=date)

        if not ok:
            abort(500)

        streak = db.get_streak(event_id=id)
        if not streak:
            ok = db.insert_streak(event_id=id)
        else:
            ok = db.update_streak(event_id=id, streak=streak[1] + 1)

        if not ok:
            abort(500)

        quote = db.get_random_quote()
        flash(f"{quote[0]} - {quote[1]}")

        return redirect(url_for("main.dashboard"))
    else:
        event = db.get_event_by_id(event_id=id, user_id=current_user.id)
        if not event:
            abort(404)

        return render_template(
            "record_event.html",
            event=event,
            form=form,
            date=date,
            is_today=(date == current_date),
        )


@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete_event(id):
    db.delete_event(id)
    return redirect(url_for("main.dashboard"))

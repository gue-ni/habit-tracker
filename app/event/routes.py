from flask import render_template, request, url_for, redirect
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
)

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    DecimalField,
)
from wtforms.validators import DataRequired, Length, EqualTo
import random

from enum import Enum

import app.db as db
from app.event import bp


class EventType(Enum):
    HABIT = "HABIT"
    QUIT = "QUIT"
    MEASURE = "MEASURE"


class EventFrequency(Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    ONE_PER_WEEK = "1_PER_WEEK"
    TWO_PER_WEEK = "2_PER_WEEK"
    THREE_PER_WEEK = "3_PER_WEEK"
    FOUR_PER_WEEK = "4_PER_WEEK"
    FIVE_PER_WEEK = "5_PER_WEEK"


class CreateEventForm(FlaskForm):
    event_name = StringField("Name", validators=[DataRequired()])
    event_emoji = SelectField(
        "Emoji",
        choices=["💪🏼", "🏃‍♂️", "️⚽", "🏋️‍♀️", "😴", "🛌", "🌙", "🎓", "🧠", "📚", "📖"],
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
        choices=["DAILY", "WEEKLY"],
        validators=[DataRequired()],
    )
    submit = SubmitField("Create")


class RecordEventForm(FlaskForm):
    numeric_value = DecimalField("Numeric Value")
    submit = SubmitField("Done")


@bp.route("/<int:id>", methods=["GET"])
def event(id):
    print(id)
    event = db.get_event_by_id(event_id=id, user_id=current_user.id)
    print(event)

    measurements = None
    occurences = None

    if event[2] == EventType.MEASURE.value:
        measurements = db.get_all_measurements(event_id=id)
        print(measurements)
    else:
        occurences = db.get_all_occurences_of_event(event_id=id)
        print(occurences)

    return render_template("event.html", event=event, occurences=occurences)


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
            event_repeat_per_week = 3

        print(event_repeat, event_repeat_per_week)

        colors = ["#ff00ff", "#ff0000", "#003366", "#4B0082"]
        hex_color = random.choice(colors)

        db.insert_event(
            event_name=event_name,
            owner=current_user.id,
            event_type=event_type,
            event_repeat=event_repeat,
            event_emoji=event_emoji,
            event_color=hex_color,
            event_description=event_description,
            event_repeat_per_week=event_repeat_per_week,
        )

        return redirect(url_for("main.dashboard"))

    else:
        return render_template("new_event.html", form=form)


@bp.route("/event/<int:id>/record", methods=["GET", "POST"])
@login_required
def record_event(id):
    form = RecordEventForm()
    if request.method == "POST":
        numeric_value = form.numeric_value.data
        print(numeric_value)
        if numeric_value:
            numeric_value = float(numeric_value)
            db.insert_measurement_of_event(event_id=id, value=numeric_value)
        else:
            db.insert_occurence_of_event(event_id=id)
        return redirect(url_for("main.dashboard"))
    else:
        event = db.get_event_by_id(event_id=id, user_id=current_user.id)
        print(event)
        return render_template("record_event.html", event=event, form=form)


@bp.route("/event/<int:id>/delete", methods=["POST"])
@login_required
def delete_event(id):
    print(f"delete {id}")
    db.delete_event(id)
    return redirect(url_for("main.dashboard"))

from flask import render_template
from app.event import bp
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
)
from enum import Enum

import app.db as db


class EventType(Enum):
    HABIT = "HABIT"
    QUIT = "QUIT"
    MEASURE = "MEASURE"


class EventFrequency(Enum):
    DAILY = "DAILY"
    THRICE_PER_WEEK = "THRICE_PER_WEEK"
    TWICE_PER_WEEK = "TWICE_PER_WEEK"
    WEEKLY = "WEEKLY"


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

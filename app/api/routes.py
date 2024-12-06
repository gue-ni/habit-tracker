from app import db
from app.api import bp
from app.utils import get_todos

from flask import jsonify
from flask_login import login_required, current_user


@bp.route("/todo")
@login_required
def api_todo():
    todo = get_todos(current_user.id)
    if todo:
        return jsonify(todo)
    else:
        return jsonify([])


@bp.route("/events")
@login_required
def api_events():
    events = db.get_all_events(current_user.id)
    if events:
        return jsonify(events)
    else:
        return jsonify([])


@bp.route("/streaks")
@login_required
def api_streaks():
    data = db.get_all_streaks_for_user(current_user.id)
    if data:
        return jsonify(data)
    else:
        return jsonify([])


@bp.route("/event/<int:event_id>/occurences")
@login_required
def api_occurences(event_id):
    event = db.get_event_by_id(event_id=event_id, user_id=current_user.id)
    if not event:
        return jsonify([])

    occurences = db.get_all_occurences_of_event(event_id=event_id)
    return jsonify(occurences)

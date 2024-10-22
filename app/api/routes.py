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

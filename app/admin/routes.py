from app.admin import bp
from app import db

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

@bp.route("/overview")
@login_required
def admin():
    if not current_user.is_admin():
       return render_template("error/404.html"), 404

    activity = db.get_all_user_activity()
    print(activity)

    return render_template("admin.html", user_activity=activity)

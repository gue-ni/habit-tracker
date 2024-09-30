from app.user import bp
from app.user.forms import SignupForm, LoginForm
from app.models import User, AppException
from app import db


import bcrypt

from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = db.get_user_by_name(username)

        if not user:
            flash("Unknown username.", "danger")

        else:
            (id, name, hashed_password) = user

            if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                new_user = User(id=id, name=name)
                remember_me = form.remember_me.data
                login_user(new_user, remember=True)
                flash("Logged in successfully.", "success")
                return redirect(url_for("main.dashboard"))
            else:
                flash("Invalid username or password.", "danger")
                return render_template("login.html", form=form), 400

    
    return render_template("login.html", form=form)

@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = db.get_user_by_name(username)

        if user:
            flash("Username already exists. Please choose a different one.", "danger")
        else:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
            ok = db.insert_user(username, hashed_password)
            if not ok:
                raise AppException("Could not insert user", 400)

            flash("You have successfully signed up! Please log in.", "success")
            return redirect(url_for("user.login"))

    return render_template("signup.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))


@bp.route("/profile")
@login_required
def profile():
    user = db.get_user_by_id(current_user.id)
    return render_template("profile.html", user=user)


@bp.route("/delete", methods=["POST"])
@login_required
def delete():
    db.delete_user(user_id=current_user.id)
    logout_user()
    return redirect(url_for("main.index"))

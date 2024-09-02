from app.user import bp
from app.user.forms import SignupForm, LoginForm
from app.models import User
from app import db


import bcrypt

from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user


@bp.route("/login_old", methods=["GET", "POST"])
def login_old():
    print(db.get_users())
    return "<h1>login</h1>"


@bp.route("/login", methods=["GET", "POST"])
def login():
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

    return render_template("login.html", form=form)


@bp.route("/signup", methods=["GET", "POST"])
def signup():
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
            db.insert_user(username, hashed_password)
            flash("You have successfully signed up! Please log in.", "success")
            return redirect(url_for("user.login"))

    return render_template("signup.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    print(f"logout {current_user}")
    logout_user()
    # session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("user.login"))

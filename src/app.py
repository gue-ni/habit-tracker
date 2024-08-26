from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
import bcrypt
import datetime
from enum import Enum
import os

import db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET", "your_secret_key_here")
app.config["REMEMBER_COOKIE_DURATION"] = datetime.timedelta(days=356)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.authenticated = False

    def is_active(self):
        return self.is_active()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    user = db.get_user_by_id(user_id)
    if not user:
        return None
    else:
        (id, name, hash) = user
        return User(int(id), name)


# @login_manager.request_loader
# def load_user_from_request(request):
#
#    # first, try to login using the api_key url arg
#    api_key = request.args.get('api_key')
#    if api_key:
#        user = User.query.filter_by(api_key=api_key).first()
#        if user:
#            return user
#
#    # next, try to login using Basic Auth
#    api_key = request.headers.get('Authorization')
#    if api_key:
#        api_key = api_key.replace('Basic ', '', 1)
#        try:
#            api_key = base64.b64decode(api_key)
#        except TypeError:
#            pass
#        user = User.query.filter_by(api_key=api_key).first()
#        if user:
#            return user
#
#    # finally, return None if both methods did not login the user
#    return None


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=25)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class SignupForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=25)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")


class EventType(Enum):
    OCCURENCE = "OCCURENCE"
    NUMERIC = "NUMERIC"


class CreateEventForm(FlaskForm):
    event_name = StringField("Event Name", validators=[DataRequired()])
    event_tag = StringField("Event Tag", validators=[DataRequired()])
    event_type = SelectField(
        "Event Type",
        choices=[(e.name, e.value) for e in EventType],
        validators=[DataRequired()],
    )
    submit = SubmitField("Create Event")


@app.route("/login", methods=["GET", "POST"])
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
                login_user(new_user, remember=remember_me)
                flash("Logged in successfully.", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid username or password.", "danger")

    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
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
            return redirect(url_for("login"))

    return render_template("signup.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    events = db.get_all_events_by_owner(current_user.id)
    return render_template("dashboard.html", user=current_user, events=events)


@app.route("/create_new_event")
@login_required
def create_new_event():
    form = CreateEventForm()
    return render_template("create_new_event.html", form=form)


@app.route("/create_event", methods=["POST"])
@login_required
def create_event():
    form = CreateEventForm()
    event_name = form.event_name.data
    event_tag = form.event_tag.data
    event_type = form.event_type.data
    print(f"create event {event_name} {event_tag}, {event_type}")
    db.insert_event(
        event_name=event_name,
        event_tag=event_tag,
        owner=current_user.id,
        event_type=event_type,
    )
    return redirect(url_for("dashboard"))


@app.route("/create_occurence", methods=["POST"])
@login_required
def create_occurence():
    id = request.args.get("id")
    data = request.get_json()
    db.insert_occurence_of_event(event_id=id)
    return redirect(url_for("dashboard"))


@app.route("/create_measurement", methods=["GET", "POST"])
@login_required
def create_measurement():
    if request.method == "POST":
        id = request.args.get("id")
        data = request.get_json()
        value = data.get("value")
        if value:
            db.insert_measurement_of_event(event_id=id, value=value)
        return redirect(url_for("dashboard"))
    else:
        return "test"


@app.route("/event/<id>", methods=["GET"])
def event(id):
    return render_template("event.html")


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

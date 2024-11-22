from enum import Enum


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired


class EventType(Enum):
    HABIT = "HABIT"
    MEASURE = "MEASURE"
    QUIT = "QUIT"


class EventFrequency(Enum):
    DAILY = "DAILY"
    ONE_PER_WEEK = "1_PER_WEEK"
    TWO_PER_WEEK = "2_PER_WEEK"
    THREE_PER_WEEK = "3_PER_WEEK"
    FOUR_PER_WEEK = "4_PER_WEEK"
    FIVE_PER_WEEK = "5_PER_WEEK"
    SIX_PER_WEEK = "6_PER_WEEK"


pretty_enum = {
    "HABIT": "Habit",
    "MEASURE": "Numeric Value",
    "QUIT": "Days Since",
    "DAILY": "Daily",
    "1_PER_WEEK": "Once Per Week",
    "2_PER_WEEK": "Twice Per Week",
    "3_PER_WEEK": "3 Times Per Week",
    "4_PER_WEEK": "4 Times Per Week",
    "5_PER_WEEK": "5 Times Per Week",
    "6_PER_WEEK": "6 Times Per Week",
}


class CreateEventForm(FlaskForm):
    emojis = [
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
        "🧹",
        "🧼",
        "🧽",
        "🧘",
    ]
    event_name = StringField("Name", validators=[DataRequired()])
    event_emoji = SelectField(
        "Emoji",
        choices=emojis,
        validators=[DataRequired()],
    )
    event_description = StringField("Description")
    event_type = SelectField(
        "Type",
        choices=[(e.value, pretty_enum[e.value]) for e in EventType],
        validators=[DataRequired()],
    )
    event_repeat = SelectField(
        "Repeat",
        choices=[(e.value, pretty_enum[e.value]) for e in EventFrequency],
        validators=[DataRequired()],
    )
    submit = SubmitField("Create")


class RecordEventForm(FlaskForm):
    numeric_value = DecimalField("Numeric Value")
    comment = StringField("Comment")
    submit = SubmitField("Done")

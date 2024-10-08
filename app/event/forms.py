from enum import Enum


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired


class EventType(Enum):
    HABIT = "HABIT"
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
            "🧹",
            "🧼",
            "🧽",
            "🧘",
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

# Habit Tracker

_Habit Tracker_ is a simple web app that helps you stick to daily or weekly
habits by tracking streaks and visualizing your progress. It can be used to
track simple occurences, like visits to the gym, or numeric data like your
bodyweight.

![Habit Tracker Screenshot](https://www.jakobmaier.at/projects/img/habit-tracker.png)

## How to run

### Development

```bash
export FLASK_APP=app
flask run --debug
```

### Production

```bash
docker compose build
docker compose up -d
```

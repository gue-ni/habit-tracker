# Habit Tracker

_Habit Tracker_ is a simple web service that is useful to track any kind of periodic
data, be it manually recording visits to the gym, or recording data points from
a sensor via a easy to use API.

On the index page, there is a simple input UI for recording an event, picked
from a list of previous event types. Every event type has it's own page, where
there are a number of different statistics that provide insight into it.

## Build

### Development

```bash
export FLASK_APP=app
flask run --debug
```

### Deployment

```bash
./init_db.sh
docker compose build
docker compose up -d
```

## Links

-   https://medium.com/analytics-vidhya/how-to-use-flask-login-with-sqlite3-9891b3248324

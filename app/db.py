import sqlite3
import datetime
import os

database = "./db/database.sqlite"


schema = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_name TEXT NOT NULL,
  event_tag TEXT,
  event_type TEXT CHECK(event_type IN ('HABIT', 'QUIT', 'MEASURE')) NOT NULL DEFAULT 'HABIT',
  event_repeat TEXT CHECK(event_repeat IN ('DAILY', 'WEEKLY')) NOT NULL DEFAULT 'DAILY',
  event_repeat_per_week INTEGER CHECK (NOT (event_repeat = 'WEEKLY' AND event_repeat_per_week IS NULL)),
  event_emoji TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  user_id INTEGER,
  description TEXT,
  hex_color TEXT DEFAULT '#FF5733',
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS occurences (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER,
  occured_at DATE DEFAULT CURRENT_DATE,
  comment TEXT,
  numeric_value FLOAT,
  UNIQUE (event_id, occured_at),
  FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS streaks (
  event_id INTEGER PRIMARY KEY,
  streak INTEGER NOT NULL DEFAULT 1,
  last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  active_since TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS quotes;

CREATE TABLE IF NOT EXISTS quotes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  quote TEXT NOT NULL,
  author TEXT NOT NULL
);

INSERT INTO quotes (quote, author) VALUES
  ('Habits change into character.', 'Ovid'),
  ('Good habits formed at youth make all the difference.', 'Aristotle'),
  ('Successful people are simply those with successful habits.', 'Brian Tracy'),
  ("Rome wasn't built in a day.", 'Unknown'),
  ("There is no elevator to success, you have to take the stairs.", "Zig Ziglar"),
  ("Our life is what our thoughts make it.", "Marcus Aurelius"),
  ("Each day provides its own gifts.", "Marcus Aurelius"),
  ("We become what we repeatedly do.", "Sean Covey"),
  ("A nail is driven out by another nail; habit is overcome by habit.", "Erasmus"),
  ("Habit is a cable; we weave a thread of it each day, and at last, we cannot break it.", "Horace Mann"),
  ("A man should be upright, not be kept upright.", "Marcus Aurelius"),
  ("First we make our habits, then our habits make us.", "Charles C. Noble"),
  ("Motivation is what gets you started. Habit is what keeps you going.", "Jim Ryun"),
  ("The chains of habit are too weak to be felt until they are too strong to be broken.", "Samuel Johnson"),
  ("Your habits will determine your future.", "Jack Canfield"),
  ("Quality is not an act, it is a habit.", "Aristotle"),
  ("The secret to permanently breaking any bad habit is to love something greater than the habit.", "Bryant McGill"),
  ("Small disciplines repeated with consistency every day lead to great achievements gained slowly over time.", "John Maxwell"),
  ("The only way you can sustain a permanent change is to create a new way of thinking, acting, and being.", "Jennifer Hudson"),
  ("Good habits are worth being fanatical about.", "John Irving"),
  ("Habit is a cable; we weave a thread of it every day, and at last we cannot break it.", "Horace Mann"),
  ("Your net worth to the world is usually determined by what remains after your bad habits are subtracted from your good ones.", "Benjamin Franklin"),
  ("The secret of your success is found in your daily routine.", "John C. Maxwell"),
  ("Motivation is what gets you started. Habit is what keeps you going.", "Jim Ryun"),
  ("Good habits, once established, are just as hard to break as bad habits.", "Robert Puller"),
  ("Change might not be fast and it isn't always easy. But with time and effort, almost any habit can be reshaped.", "Charles Duhigg"),
  ("The difference between an amateur and a professional is in their habits. An amateur has amateur habits. A professional has professional habits.", "Steven Pressfield"),
  ("The best way to break a bad habit is to drop it.", "Leo Aikman");
"""


def fetchall(query, params=()):
    con = None
    try:
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"An error occured: {e}")
    finally:
        if con:
            con.close()

    return None


def fetchone(query, params=()):
    con = None
    try:
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute(query, params)
        row = cur.fetchone()
        return row
    except Exception as e:
        print(f"An error occured: {e}")
    finally:
        if con:
            con.close()

    return None


def execute(query, params=()):
    con = None
    try:
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute(query, params)
        con.commit()
        return True
    except Exception as e:
        print(f"An error occured: {e}")
    finally:

        if con:
            con.close()

    return False


def get_last_monday():
    today = datetime.date.today()
    last_monday = today - datetime.timedelta(days=today.weekday())
    return last_monday.strftime("%Y-%m-%d")


def get_yesterday():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def get_current_date():
    today = datetime.date.today()
    return today.strftime("%Y-%m-%d")


def create_db():
    dirname = os.path.dirname(database)

    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    conn = sqlite3.connect(database)

    try:
        with conn:
            conn.executescript(schema)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()


def delete_user(user_id):
    query = "DELETE FROM users WHERE id = ?"
    return execute(query, (user_id,))


def insert_user(username, password):
    query = "INSERT INTO users (name, password) VALUES (?,?)"
    return execute(query, (username, password))


def update_password(user_id, new_password):
    query = "UPDATE users SET password = ? WHERE id = ?"
    return execute(query, (new_password, user_id))


def get_users():
    query = "SELECT name, password FROM users"
    return fetchall(query)


def get_user_by_name(username):
    query = "SELECT id, name, password FROM users WHERE name = ?"
    return fetchone(query, (username,))


def get_user_by_id(id):
    query = "SELECT id, name, password, joined FROM users WHERE id = ?"
    return fetchone(query, (id,))


def insert_event(
    event_name,
    owner,
    event_type,
    event_repeat,
    event_emoji,
    event_color,
    event_description,
    event_repeat_per_week=0,
):
    query = "INSERT INTO events (event_name, user_id, event_type, event_repeat, event_emoji, hex_color, description, event_repeat_per_week) VALUES (?,?,?,?,?,?,?,?)"
    return execute(
        query,
        (
            event_name,
            owner,
            event_type,
            event_repeat,
            event_emoji,
            event_color,
            event_description,
            event_repeat_per_week,
        ),
    )


def delete_event(event_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "DELETE FROM events WHERE id = ?"
    cur.execute(
        query,
        (event_id,),
    )
    con.commit()
    con.close()


def get_todo_daily_events(user_id):
    query = """
        SELECT e.id, e.event_name, e.event_type, e.event_emoji, e.description, e.event_repeat, e.hex_color
        FROM events e
        LEFT JOIN occurences o ON e.id = o.event_id and date(o.occured_at) = CURRENT_DATE
        WHERE o.occured_at IS NULL AND e.event_repeat = 'DAILY' AND user_id = ?
    """
    return fetchall(query, (user_id,))


def get_todo_weekly_events(user_id, current_date, last_monday=get_last_monday()):
    query = """
        SELECT e.id, e.event_name, e.event_type, e.event_emoji, e.description, e.event_repeat, e.hex_color, COUNT(o.id) AS count, e.event_repeat_per_week, MAX(o.occured_at) AS last
        FROM events e
        LEFT JOIN
        (SELECT * FROM occurences WHERE occured_at >= DATE(?)) AS o
        ON e.id = o.event_id
        WHERE e.user_id = ? AND e.event_repeat = 'WEEKLY'
        GROUP BY e.id
        HAVING (count < e.event_repeat_per_week) AND ((last < DATE(?)) OR (last IS NULL))
    """

    return fetchall(
        query,
        (last_monday, user_id, current_date),
    )


def get_all_events(user_id):
    query = """
        SELECT e.id, e.event_name, e.event_type, e.event_emoji, e.description, e.event_repeat, e.hex_color, ifnull(s.streak, 0)
        FROM events e
        LEFT JOIN streaks s ON e.id = s.event_id
        WHERE e.user_id = ?
        ORDER BY s.streak DESC
        """
    return fetchall(query, (user_id,))


def get_event(event_id):
    query = "SELECT id, event_name, event_type, event_emoji, description, event_repeat, hex_color, event_repeat_per_week FROM events WHERE id = ?"
    return fetchone(
        query,
        (event_id,),
    )


def get_event_by_id(user_id, event_id):
    query = "SELECT id, event_name, event_type, event_emoji, description, event_repeat, hex_color, event_repeat_per_week FROM events WHERE user_id = ? AND id = ?"
    return fetchone(
        query,
        (
            user_id,
            event_id,
        ),
    )


def insert_occurence_of_event(event_id, date, comment=""):
    query = "INSERT INTO occurences (event_id, occured_at, comment) VALUES (?, ?, ?)"
    return execute(
        query,
        (
            event_id,
            date,
            comment,
        ),
    )


def insert_measurement_of_event(event_id, value, date, comment=""):
    query = "INSERT INTO occurences (event_id, numeric_value, occured_at, comment) VALUES (?, ?, ?, ?)"
    return execute(
        query,
        (
            event_id,
            value,
            date,
            comment,
        ),
    )


def get_all_occurences_of_event(event_id):
    query = "SELECT id, occured_at, numeric_value FROM occurences WHERE event_id = ? ORDER BY occured_at"
    return fetchall(
        query,
        (event_id,),
    )


def get_all_measurements(event_id):
    query = "SELECT occured_at, numeric_value FROM occurences WHERE event_id = ? AND numeric_value NOT NULL ORDER BY occured_at"
    return fetchall(query, (event_id,))


def get_streak(event_id):
    query = "SELECT event_id, streak FROM streaks WHERE event_id = ?"
    return fetchone(
        query,
        (event_id,),
    )


def insert_streak(event_id, streak=1):
    query = "INSERT INTO streaks (event_id, streak) VALUES (?, ?)"
    return execute(
        query,
        (
            event_id,
            streak,
        ),
    )


def update_streak(event_id, streak):
    query = "UPDATE streaks SET streak = ? WHERE event_id = ?"
    return execute(
        query,
        (
            streak,
            event_id,
        ),
    )


def delete_streak(event_id):
    query = "DELETE FROM streaks WHERE event_id = ?"
    return execute(
        query,
        (event_id,),
    )


def get_all_occurances_between(event_id, start_date, end_date):
    query = "SELECT o.event_id, o.occured_at FROM occurences o WHERE o.event_id = ? AND DATE(?) <= o.occured_at AND o.occured_at < DATE(?) ORDER BY o.occured_at"
    return fetchall(
        query,
        (
            event_id,
            start_date,
            end_date,
        ),
    )
    return result


def get_all_occurances(event_id):
    query = "SELECT o.event_id, o.occured_at FROM occurences o WHERE o.event_id = ? ORDER BY o.occured_at"
    return fetchall(query, (event_id,))


def get_all_occurences(event_id):
    query = "SELECT o.event_id, o.occured_at FROM occurences o WHERE o.event_id = ? ORDER BY o.occured_at"
    return fetchall(query, (event_id,))


def get_streaks_to_recompute(user_id):
    query = """
      SELECT e.id, e.event_name, s.streak, s.last_updated_at
      FROM streaks s
      JOIN events e
      ON s.event_id = e.id
      WHERE
      e.user_id = ?
      AND DATE(s.last_updated_at) < DATE('now')
   """
    return fetchall(query, (user_id,))


def get_all_streaks_for_user(user_id):
    query = """
      SELECT e.id, e.event_name, s.streak, s.last_updated_at
      FROM streaks s
      JOIN events e ON s.event_id = e.id
      WHERE
      e.user_id = ?
    """
    return fetchall(query, (user_id,))


def get_random_quote():
    query = "SELECT quote, author FROM quotes ORDER BY RANDOM() LIMIT 1"
    return fetchone(query)

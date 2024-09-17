import sqlite3
import datetime


database = "./db/database.sqlite"


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


def insert_user(username, password):
    query = "INSERT INTO users (name,password) VALUES (?,?)"
    execute(query, (username, password))


def get_users():
    query = "SELECT name, password FROM users"
    return fetchall(query)


def get_user_by_name(username):
    query = "SELECT id, name, password FROM users WHERE name = ?"
    return fetchone(query, (username,))


def get_user_by_id(id):
    query = "SELECT id, name, password FROM users WHERE id = ?"
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


def get_todo_weekly_events(user_id):
    last_monday = get_last_monday()

    query = """SELECT sub.id, sub.event_name, sub.event_type, sub.event_emoji, sub.description, sub.event_repeat, sub.hex_color, sub.cnt, sub.last_occured FROM
                (
                    SELECT e.id, e.event_name, e.event_type, e.event_emoji, e.description, e.event_repeat, e.hex_color, e.event_repeat_per_week, COUNT(o.id) as cnt, o.occured_at, e.user_id, MAX(o.occured_at) AS last_occured
                    FROM events e
                    LEFT JOIN occurences o
                    ON e.id = o.event_id
                    GROUP BY e.id
                    HAVING DATE(?) <= o.occured_at OR o.occured_at IS NULL
                ) AS sub
                WHERE
                    sub.event_repeat = 'WEEKLY'
                    AND sub.user_id = ?
                    AND sub.cnt < sub.event_repeat_per_week
                    AND (sub.last_occured IS NULL OR sub.last_occured != CURRENT_DATE)
            """

    query2 = """
        SELECT e.id, e.event_name, e.event_type, e.event_emoji, e.description, e.event_repeat, e.hex_color, e.event_repeat_per_week, COUNT(o.id) as cnt, o.occured_at, e.user_id, MAX(o.occured_at) AS last_occured
        FROM events e
        LEFT JOIN occurences o
        ON e.id = o.event_id
        GROUP BY e.id
        HAVING (DATE(?) <= o.occured_at OR o.occured_at IS NULL) AND (e.user_id = ?) AND (e.event_repeat = 'WEEKLY')
    """

    return fetchall(query2, (last_monday, user_id))


def get_all_events(user_id):
    query = """
        SELECT e.id, e.event_name, e.event_type, e.event_emoji, e.description, e.event_repeat, e.hex_color, ifnull(s.streak, 0)
        FROM events e
        LEFT JOIN streaks s ON e.id = s.event_id
        WHERE e.user_id = ?
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


def insert_occurence_of_event(event_id, date):
    query = "INSERT INTO occurences (event_id, occured_at) VALUES (?, ?)"
    return execute(query, (event_id, date,))


def insert_measurement_of_event(event_id, value, date):
    query = "INSERT INTO occurences (event_id, numeric_value) VALUES (?, ?, ?)"
    return execute(
        query,
        (
            event_id,
            value,
            date,
        ),
    )


def get_all_occurences_of_event(event_id):
    query = "SELECT id, occured_at FROM occurences WHERE event_id = ?"
    return fetchall(
        query,
        (event_id,),
    )


def get_all_measurements(event_id):
    query = "SELECT occured_at, numeric_value FROM occurences WHERE event_id = ? AND numeric_value NOT NULL"
    return fetchall(query, (event_id,))


def get_streak(event_id):
    query = "SELECT event_id, streak FROM streaks WHERE event_id = ?"
    return fetchone(
        query,
        (event_id,),
    )


def insert_streak(event_id):
    query = "INSERT INTO streaks (event_id, streak) VALUES (?, 1)"
    return execute(
        query,
        (event_id,),
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
    query = "SELECT o.event_id, o.occured_at FROM occurences o WHERE o.event_id = ? AND DATE(?) <= o.occured_at AND o.occured_at < DATE(?)"
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
    query = "SELECT o.event_id, o.occured_at FROM occurences o WHERE o.event_id = ?"
    return fetchall(query, (event_id,))


def get_all_occurences(event_id):
    query = "SELECT o.event_id, o.occured_at FROM occurences o WHERE o.event_id = ?"
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

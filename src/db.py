import sqlite3

database = "./db/database.sqlite"


def insert_user(username, password):
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "INSERT INTO users (name,password) VALUES (?,?)"
    cur.execute(query, (username, password))
    con.commit()
    con.close()


def get_users():
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "SELECT name, password FROM users"
    cur.execute(query)
    users = cur.fetchall()
    con.close()
    return users


def get_user_by_name(username):
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "SELECT id, name, password FROM users WHERE name = ?"
    cur.execute(query, (username,))
    user = cur.fetchone()
    con.commit()
    con.close()
    return user


def get_user_by_id(id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "SELECT id, name, password FROM users WHERE id = ?"
    cur.execute(query, (id,))
    user = cur.fetchone()
    con.commit()
    con.close()
    return user


def insert_event(
    event_name,
    owner,
    event_type,
    event_repeat,
    event_emoji,
    event_color,
):
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "INSERT INTO events (event_name, user_id, event_type, event_repeat, event_emoji, hex_color) VALUES (?,?,?,?,?,?)"
    cur.execute(
        query,
        (event_name, owner, event_type, event_repeat, event_emoji, event_color),
    )
    con.commit()
    con.close()


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

def get_todo_events(user_id):
    query = "select e.event_name, o.occured_at from events e left join occurences o on e.id = o.event_id and date(o.occured_at) = CURRENT_DATE where o.occured_at is null;"

def get_all_events_by_owner(user_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "SELECT id, event_name, event_type, event_emoji, description, event_repeat, hex_color FROM events WHERE user_id = ?"
    cur.execute(query, (user_id,))
    result = cur.fetchall()
    con.close()
    return result


def get_event_by_id(user_id, event_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "SELECT id, event_name, event_type, event_emoji, description, event_repeat, hex_color FROM events WHERE user_id = ? AND id = ?"
    cur.execute(
        query,
        (
            user_id,
            event_id,
        ),
    )
    result = cur.fetchone()
    con.close()
    return result


def insert_occurence_of_event(event_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "INSERT INTO occurences (event_id) VALUES (?)"
    cur.execute(query, (event_id,))
    con.commit()
    con.close()


def insert_measurement_of_event(event_id, value):
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "INSERT INTO occurences (event_id, numeric_value) VALUES (?,?)"
    cur.execute(
        query,
        (
            event_id,
            value,
        ),
    )
    con.commit()
    con.close()


def get_all_occurences_of_event(event_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "SELECT id, occured_at FROM occurences WHERE event_id = ?"
    cur.execute(
        query,
        (event_id,),
    )
    result = cur.fetchall()
    con.close()
    return result


def get_all_measurements(event_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "SELECT occured_at, numeric_value FROM occurences WHERE event_id = ? AND numeric_value NOT NULL"
    cur.execute(
        query,
        (event_id,),
    )
    result = cur.fetchall()
    con.close()
    return result

import sqlite3

database = "/home/pi/clock-in/db/database.sqlite"


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


def insert_event(event_name, event_tag, owner, event_type):
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = (
        "INSERT INTO events (event_name,event_tag,user_id,event_type) VALUES (?,?,?,?)"
    )
    cur.execute(query, (event_name, event_tag, owner, event_type))
    con.commit()
    con.close()


def get_all_events_by_owner(user_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "SELECT id, event_name, event_tag, event_type FROM events WHERE user_id = ?"
    cur.execute(query, (user_id,))
    result = cur.fetchall()
    con.close()
    return result

def get_event_by_id(user_id, event_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = "SELECT id, event_name, event_tag, event_type FROM events WHERE user_id = ? AND id = ?"
    cur.execute(query, (user_id, event_id, ))
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
    query = "INSERT INTO measurements (event_id, value) VALUES (?,?)"
    cur.execute(
        query,
        (
            event_id,
            value,
        ),
    )
    con.commit()
    con.close()

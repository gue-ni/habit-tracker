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


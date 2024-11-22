import bcrypt
import sqlite3
import sys

username = sys.argv[1]
password = sys.argv[2]

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

db = "db/database.sqlite"

con = sqlite3.connect(db)
cur = con.cursor()

query = "update users set password = ? where name = ?"
cur.execute(query, (hashed, username))

con.commit()
con.close()

print(f"Password for user '{username}' has been changed.")
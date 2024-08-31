import sqlite3

conn = sqlite3.connect("db/database.sqlite")

try:
    with open("app/schema.sql", "r") as file:
        schema = file.read()

    with conn:
        conn.executescript(schema)

    print("Schema executed successfully.")
    print(schema)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    conn.close()

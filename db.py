import sqlite3



conn = sqlite3.connect("test.db")

# create a cursor
# cursor -> a pointer to a record
cursor = conn.cursor()


# execute -> execute a sql statement
cursor.execute("""
    CREATE TABLE IF NOT EXISTS TODO (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title text,
        completed boolean,
        date_created datetime
    );
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS USER (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username varchar(40),
        password text
        );
""")

query = """
    INSERT INTO USER (username, password)
    VALUES (:username, :password)
"""

cursor.execute(query, {"username": "admin", "password": "admin"})

conn.commit()
conn.close()
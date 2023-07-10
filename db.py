import sqlite3


conn = sqlite3.connect("test.db")

# create a cursor
# cursor -> a pointer to a record
cursor = conn.cursor()


# execute -> execute a sql statement
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS TODO (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title text,
        completed boolean,
        date_created datetime
    );
"""
)


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS USER (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username varchar(40),
        password text
        );
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS SESSIONS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key text,
        user_id integer,
        FOREIGN KEY(user_id) REFERENCES USER(id) ON DELETE CASCADE
        );
"""
)


cursor.execute(
    """
    ALTER TABLE USER ADD UNIQUE (username)

               """
)

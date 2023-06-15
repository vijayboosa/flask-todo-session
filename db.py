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



# insert data to db
fake_data = {"title": "Learn Python", "completed": False, "date_created": "2023-06-15"}


query = """
    INSERT INTO TODO (title, completed, date_created)
    VALUES (:title, :completed, :date_created)
"""

cursor.execute(query, fake_data)


conn.commit() # commit -> save changes
conn.close() # close -> close connection to db
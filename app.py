from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime


app = Flask(__name__)


# / -> home page a
@app.route("/", methods=['GET', 'POST'])
def home():
    
    if (request.method == "GET"):
        # get the data from the database 
        # all todos from the db
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()
        
        query = """
            SELECT * FROM TODO
        """
        
        cursor.execute(query)
        
        todos = cursor.fetchall() # fetchall -> get all the data from the cursor
        # [(1, "buy eggs", False, "d"), (), ()]
        
        return render_template("home.html", todos=todos)
    
    # handle post request
    form_data = request.form
    title = form_data.get("title", default="").strip()
    
    if len(title) <= 0:
        return redirect("/")

    
    # save the data to the database
    conn = sqlite3.connect("test.db")
    
    # create a cursor
    cursor = conn.cursor()
    
    query = """
        INSERT INTO TODO (title, completed, date_created)
        VALUES (:title, :completed, :date_created)
    """
    
    cursor.execute(query, 
                   {"title": title, "completed": False, "date_created":datetime.now()})
    
    print("Data saved to db")
    # save changes
    conn.commit()
    # redirect to home page
    return redirect("/")
        
    

# /add-todo -> add todo page


# /delete-todo -> delete todo page
@app.route("/delete-todo/<int:todo_id>", methods=['POST'])
def delete_todo(todo_id):
    # connect to the database
    conn = sqlite3.connect("test.db")
    
    # create a cursor
    cursor = conn.cursor()
    
    query = """
        DELETE FROM TODO WHERE id = :todo_id
    """
    
    cursor.execute(query, {"todo_id": todo_id})
    
    # save changes
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/todo-completed/<int:todo_id>", methods=['POST'])
def todo_completed(todo_id):
    print(request.form)
    return redirect("/")


# /update-todo -> update todo page





app.run(debug=True)
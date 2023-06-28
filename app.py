from flask import Flask, render_template, request, redirect,make_response
import sqlite3
from datetime import datetime
import re


app = Flask(__name__)

def generate_session_token():
    from random import choices
    import string
    
    key = ''.join(choices(string.ascii_letters + string.digits, k=50))
    
    return key


def get_token_from_request():
    return request.cookies.get("token", default=None)

def verify_token(token):
    conn = sqlite3.connect("test.db")
    
    cursor = conn.cursor()
    
    query = """
        SELECT user_id FROM SESSIONS WHERE key = :key
        """

    cursor.execute(query, {"key": token})
    
    result = cursor.fetchone()
    
    result = result[0] if result else None
    
    return result
    

# / -> home page a
@app.route("/", methods=['GET', 'POST'])
def home():
    
    if (request.method == "GET"):
        
        #TODO check if the user is logged in by checking the cookie
        
        #TODO verify the token in the cookie whether it is valid or not
        
        #TODO if not valid -> redirect to login page
        
        
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


@app.route("/todo-completed/<int:todo_id>")
def todo_completed(todo_id):

    # connect to db
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    
    # write a query to update the todo column completed to True or False where id = todo_id
    query = """
        UPDATE TODO SET completed = 
        CASE WHEN completed = 1 THEN 
            0
        ELSE 
            1
        END
        WHERE id = :todo_id;
    """
    
    cursor.execute(query, { "todo_id": todo_id})
    
    # save changes
    conn.commit()
    
    return {"message": "todo completed"}



@app.route('/login', methods=['GET', 'POST'])
def login():
    
    token = get_token_from_request()
        
    if token:
        # check in the database if the token is valid
        result = verify_token(token)
        if result:
            return redirect("/")

    
    if request.method == "POST":
        
        response_home = make_response(redirect("/"))
        response_login = make_response(redirect("/login"))
        
        response_login.delete_cookie("token")

        # get the username and password from the form
        username = request.form.get("username", default="").strip()
        pwd = request.form.get("password", default="").strip()
        
        # if username or password is empty -> redirect to login page
        if len(username) <= 0 or len(pwd) <= 0:
            return response_login
        
        # check if the username and password are valid with 
        # the database
        conn = sqlite3.connect("test.db")
        
        cursor = conn.cursor()
        
        query = "select id from USER where username = :username and password = :password"
        # username -> abhi
        # pwd -> abhi
        cursor.execute(query, {"username": username, "password": pwd})
        
        result = cursor.fetchone() 
        # result -> (1,) if user exists
        # result -> None -> if user does not exist

        if result:
            token = generate_session_token()
            
            # set the cookie in the sessions table
            query = """
                INSERT INTO SESSIONS (key, user_id) 
                VALUES (:key, :user_id)
            """
            cursor.execute(query, {"key": token, "user_id": result[0]})
            conn.commit()
            

            response_home.set_cookie("token", token)
            
            return response_home
        
        return redirect("/login")
    
    response = make_response(render_template("login.html"))
    response.delete_cookie("token")     
    return response



app.run(debug=True)
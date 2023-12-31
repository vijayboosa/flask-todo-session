from flask import Flask, render_template, request, redirect, make_response
import sqlite3
from datetime import datetime
import re


app = Flask(__name__)


def generate_session_token():
    from random import choices
    import string

    key = "".join(choices(string.ascii_letters + string.digits, k=50))

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


def login_required(fun):
    def wrapper(*args, **kwargs):
        # TODO check if the user is logged in by checking the cookie
        token = get_token_from_request()

        if token is None:
            response = make_response(redirect("/login"))
            response.delete_cookie("token")
            return response

        # TODO verify the token in the cookie whether it is valid or not
        if verify_token(token) is None:
            response = make_response(redirect("/login"))
            response.delete_cookie("token")
            return response
        return fun(*args, **kwargs)

    return wrapper


@app.route("/logout")
def logout():
    response = make_response(redirect("/login"))
    response.delete_cookie("token")

    return response


# / -> home page a
@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "GET":
        # get the data from the database
        # all todos from the db
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()

        query = """
            SELECT * FROM TODO
        """

        cursor.execute(query)

        todos = cursor.fetchall()  # fetchall -> get all the data from the cursor
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

    token = request.cookies.get("token")

    user_id_query = "SELECT user_id from SESSIONS WHERE key = :key"

    cursor.execute(user_id_query, {"key": token})

    user_id = cursor.fetchone()[0]  # (3,)

    query = """
        INSERT INTO TODO (title, completed, date_created, user_id)
        VALUES (:title, :completed, :date_created, :user_id)
    """

    cursor.execute(
        query,
        {
            "title": title,
            "completed": False,
            "date_created": datetime.now(),
            "user_id": user_id,
        },
    )

    print("Data saved to db")
    # save changes
    conn.commit()
    # redirect to home page
    return redirect("/")


# /add-todo -> add todo page


# /delete-todo -> delete todo page
@app.route("/delete-todo/<int:todo_id>", methods=["POST"])
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

    cursor.execute(query, {"todo_id": todo_id})

    # save changes
    conn.commit()

    return {"message": "todo completed"}


@app.route("/login", methods=["GET", "POST"])
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

        query = (
            "select id from USER where username = :username and password = :password"
        )
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


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        msg = request.args.get("msg")
        username = request.args.get("username")
        error = request.args.get("error")
        return render_template(
            "signup.html", context={"msg": msg, "name": username, "err": error}
        )

    form_data = request.form
    username = form_data.get("username")
    password = form_data.get("password")
    confirm_password = form_data.get("confirm-password")

    if password != confirm_password:
        return redirect(
            f"/signup?msg=password doesn't match&username={username}&error=pwd"
        )

    # check if the username already exists in the database
    conn = sqlite3.connect("test.db")

    cursor = conn.cursor()

    query = """
        SELECT id FROM USER WHERE username = :username
    """
    cursor.execute(query, {"username": username.strip()})
    result = cursor.fetchone()
    if result:
        return redirect(
            f"/signup?msg=username already exists&username={username}&error=username"
        )

    # insert the username and password in the database
    query = " INSERT INTO USER (username, password) VALUES (:username, :password)"
    cursor.execute(query, {"username": username, "password": password})

    conn.commit()

    return redirect("/login")


app.run(debug=True, port=8080)

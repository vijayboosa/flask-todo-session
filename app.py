from flask import Flask, render_template, request, redirect


app = Flask(__name__)


# / -> home page a
@app.route("/", methods=['GET', 'POST'])
def home():
    if (request.method == "GET"):
        return render_template("home.html")
    
    # handle post request
    form_data = request.form
    title = form_data.get("title", default="").strip()
    
    if len(title) <= 0:
        return redirect("/")

    
    # save the data to the database
    
    
    # redirect to home page
    return redirect("/")
        
    

# /add-todo -> add todo page


# /delete-todo -> delete todo page


# /update-todo -> update todo page





app.run(debug=True)
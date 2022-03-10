from flask import Flask, render_template, request, redirect, session, get_flashed_messages
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

'''HOME'''
@app.route("/")
def index():
    return render_template("index.html")


'''READ ALL'''
@app.route("/users/read")
def read_users():
    results = User.select_all()
    return render_template("users.html", output=results)


'''READ ONE'''
@app.route("/user/read/<id>")
def read_user(id):
    data={"id": id}
    element = User.select_one(data)
    results = Recipe.select_all()
    return render_template("user.html", element=element, output=results)

'''login'''
@app.route("/user/login", methods=["POST"])
def login():
    data = request.form
    # 1) get immutable dictionary from form 
    if not User.validate_login(data):
    # 2) if validate login form data == False
        return redirect("/user/login_register")
        # 4) redirect to form
    else:
    # 2) if validate login form data == True
        session["logged_in"] = User.get_email(data)
        # 3) declare session logged in variable
        # 3) assign result of get_email() 
        # 3) using data dict from form
        return redirect(f"/user/read/{session['logged_in']['id']}")
        # 4) return to logged in dashboard


'''CREATE'''
@app.route("/user/login_register")
def create_user():
# create new user == REGISTER
    return render_template("login.html")

'''register'''
@app.route("/user/create/process", methods=["POST"])
def create_process():
# create new user == REGISTER
    data={k:v for k,v in request.form.items()}
    if not User.validate_insert(data):
        return redirect("/user/login_register")
    else:
        data["password"] = bcrypt.generate_password_hash(request.form["password"])
        User.insert(data)
        session['logged_in'] = User.get_email(data)
        return redirect(f"/user/read/{session['logged_in']['id']}")

'''logout'''
@app.route("/user/logout")
def logout():
    session.clear()
    return redirect("/")



'''CATCHALL'''
@app.route("/", defaults={"path":""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("catchall.html")
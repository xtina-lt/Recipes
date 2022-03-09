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
    print(data)
    if not User.validate_login(data):
        return redirect("/user/login_register")
    else:
        session["logged_in"] = User.get_email(data)
        print(session["logged_in"])
    return redirect(f"/user/read/{session['logged_in']}")


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
        session['logged_in'] = User.insert(data)
        print(session["logged_in"])
    return redirect(f"/user/read/{session['logged_in']}")

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
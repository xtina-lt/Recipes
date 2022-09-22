from cmath import log
from flask import Flask, render_template, request, redirect, session, get_flashed_messages
# 1) import get_flashed_messages
from flask_app import app
# 0 ) import app
from flask_app.models.user import User
# 0 ) import model user
from flask_app.models.recipe import Recipe
# 0 ) import model recipe
from flask_bcrypt import Bcrypt
# 2) import Bcrypt object
bcrypt=Bcrypt(app)
# 2) initialze new Bcrypt object using app

'''HOME'''
@app.route("/")
def index():
    return render_template("index.html")

############################
'''LOGIN AND REGISTRATION'''
############################
'''show'''
@app.route("/user/login_reg")
def create_user():
# create new user == REGISTER
# 1) show login / show register
    return render_template("login.html")

'''login'''
@app.route("/user/login/process", methods=["POST"])
def login():
    data = request.form
    # 1) get immutable dictionary from form 
    if not User.validate_login(data):
    # 2) if validate login form data == False
        return redirect("/user/login_reg")
        # 4) redirect to form
    else:
    # 2) if validate login form data == True
        session["logged_in"] = User.get_email(data)
        # 3) declare session logged in variable
        # 3) assign result of get_email() 
        # 3) using data dict from form
        return redirect(f"/user/{session['logged_in']['id']}/dash")
        # 4) return to logged in dashboard

'''register'''
@app.route("/user/reg/process", methods=["POST"])
def create_process_lets_go():
    # create new user == REGISTER
    data={k:v for k,v in request.form.items()}
    # 2) get mutabale dictionary from form
    if not User.validate_insert(data):
    # 3) validate == False
        return redirect("/user/login_reg")
        # 7) go back to form
        
    else:
    # 3) validate == True
        data["password"] = bcrypt.generate_password_hash(request.form["password"])
        # 4) hash password
        User.insert(data)
        # 5) insert form data into users 
        session['logged_in'] = User.get_email(data)
        # 6) get user information by email from data
        # 6) save as logged in session
        return redirect("/dashboard")
        # return redirect(f"/user/{session['logged_in']['id']}/dash")
        # 7) go to new user's dashboard

'''logout'''
@app.route("/user/logout")
def logout():
    session.clear()
    # 1) .clear() method
    return redirect("/")

##########
'''READ'''
##########
'''read all'''
@app.route("/users")
def read_users():
    results = User.select_all()
    return render_template("users.html", output=results)

'''read one/dashboard'''
@app.route("/user/<id>/dash")
def dashboard(id):
    data={"id": int(id)}
    element = User.select_one(data)
    results = Recipe.select_all()
    return render_template("dash.html", element=element, output=results)



'''CATCHALL'''
@app.route("/", defaults={"path":""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("catchall.html")
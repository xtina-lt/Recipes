from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")

class User:
    db = 'recipes_schema'
    def __init__(self,data):
        self.id=data["id"]
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.email=data["email"]
        self.password=data["password"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
    
    '''READ ALL'''
    @classmethod
    def select_all(cls):
        query="SELECT * FROM users"
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(i) for i in results]

    '''READ ONE'''
    @staticmethod
    def validate_login(e):
        is_valid=True
        email=User.get_email(e)
        if email:
            check_me = User.select_one(email)
            if not bcrypt.check_password_hash(check_me.password, e["password"]):
                flash("Incorrect password", "login")
                is_valid=False
            return is_valid
        else:
            flash("Not a valid email", "login")
            is_valid=False
            return is_valid



    @classmethod
    def select_one(cls, data):
        query="SELECT * FROM users WHERE id=%(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_email(cls, data):
        query="SELECT * FROM users WHERE email=%(email)s"
        result = connectToMySQL(cls.db).query_db(query,data)
        if result:
            print(cls(result[0]))
            return result[0]
        else:
            return False
    

    
    '''CREATE'''
    @staticmethod
    def validate_insert(e):
        is_valid=True
        '''first/last name lengths'''
        if len(e["first_name"]) < 3:
            flash("First name should be greater than 3 characters", "register")
            is_valid=False
        if len(e["last_name"]) < 3:
            flash("Last name should be greater than 3 characters", "register")
            is_valid=False
        '''email'''
        if not EMAIL_REGEX.match(e["email"]):
            flash("Not a valid email", "register")
            is_valid=False
        if e["email"] != e["check_email"]:
            flash("Emails are not the same", "register")
            is_valid=False
        if User.get_email(e):
            flash("Email in use 😞", "register")
            is_valid= False
        '''password'''
        if e["password"] != e["check_pword"]:
            flash("Passwords do not match", "register")
            is_valid=False
        if not PASSWORD_REGEX.match(e["password"]):
            flash("Password must contain: 1 upper, 1 lower, 1 special character, 1 number.", "register")
            is_valid = False
        return is_valid

    @classmethod
    def insert(cls, data):
        query="INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.db).query_db(query, data)
        # returns id

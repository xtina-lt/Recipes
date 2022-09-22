from flask_app.config.mysqlconnection import connectToMySQL
# 0) import connectToMySQL to connect to db
from flask import flash
# 1) import flash messages
from flask_bcrypt import Bcrypt
# 2) import Bcrypt object for hashing
from flask_app import app
# 2) import app to make into Bcrypt object
bcrypt = Bcrypt(app)
# 2) instantiate app as Bcrypt object
import re
# 3) import Regular Expression
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
# 3) declare email regex variable assign format
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
# 3) declare password regex variable assign format

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

    ##############
    '''READ ONE'''
    ##############
    '''get one by email'''
    @classmethod
    def get_email(cls, data):
        query="SELECT * FROM users WHERE email=%(email)s"
        result = connectToMySQL(cls.db).query_db(query,data)
        if result:
        # 1) if email
            return result[0]
            # 2) return first dictionary in list
        else:
        # 1) if no email
            return False
            # 2) return false

    '''read one'''
    @classmethod
    def select_one(cls, data):
        print(data)
        query="SELECT * FROM users WHERE id=" + str(data)
        print(query)
        result = connectToMySQL(cls.db).query_db(query)
        print('result', result)
        return result[0]
        # instatiate class object 
        # with first dictionary in list
            
    '''validate read_one()'''
    @staticmethod
    def validate_login(e):
        is_valid=True
        # 1) declare is_valid variabe
        # 1) assign True value
        email=User.get_email(e)
        # 2) use form data
        # 2) get user by email
        # 2) set dict value as declared email variable
        if email:
        # 3) if an email is found
            if not bcrypt.check_password_hash(email['password'], e["password"]):
            # 4) check user db data already hashed password
            # 4) compare with form password to hash
                flash("Incorrect password", "login")
                # 5) flash message
                # 5) set message CATEGORY
                is_valid=False
                # 6) change is valid value
            return is_valid
            # 7) return is_Valid variable
        else:
        # 3) if an email is not found
            flash("Not a valid email", "login")
            # 5) flash message
            # 5) set message CATEGORY
            is_valid=False
            # 6) change is_valid value
            return is_valid
            # 7) return is_valid variable

    #######################
    '''CREATE / REGISTER'''
    #######################
    '''create'''
    @classmethod
    def insert(cls, data):
        query="INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.db).query_db(query, data)
        # returns id

    '''validate create'''
    @staticmethod
    def validate_insert(e):
        is_valid=True
        # 1) declare is valid
        # 1) assign True value
        '''first/last name lengths'''
        # 2) NAME LENGTHS
        if len(e["first_name"]) < 3:
        # 2a) check length
            flash("First name should be greater than 3 characters", "register")
            # b) set flash message and category
            is_valid=False
            # c) change is_Valid value
        if len(e["last_name"]) < 3:
        # 2a) check length
            flash("Last name should be greater than 3 characters", "register")
            # b) set flash message and category
            is_valid=False
            # c) change is_valid value
        '''email'''
        # 3) EMAILS
        if not EMAIL_REGEX.match(e["email"]):
        # 3a) compare email to regex format
            flash("Not a valid email", "register")
            # b) set flash message and category
            is_valid=False
            # c) change is_valid value
        if e["email"] != e["check_email"]:
        # 3a) compare confirm email
            flash("Emails are not the same", "register")
            # b) set flash message and category
            is_valid=False
            # c) change is_valid value
        if User.get_email(e):
        # 3a) if the email from the form
        # 3a) is already in database
            flash("Email in use 😞", "register")
            # b) set flash message and category
            is_valid= False
            # c) change is_valid value
        '''password'''
        # 4) PASSWORDS
        if e["password"] != e["check_pword"]:
        # 4a) compare confirm password
            flash("Passwords do not match", "register")
            # b) set flash message and category
            is_valid=False
            # c) change is_valid value
        if not PASSWORD_REGEX.match(e["password"]):
        # 4a) compare email to regex format
            flash("Password must contain: 1 upper, 1 lower, 1 special character, 1 number.", "register")
            # b) set flash message and category
            is_valid = False
            # c) change is_valid value
        return is_valid
        # 5) return is_valid value

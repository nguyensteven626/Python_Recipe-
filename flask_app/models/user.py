from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class User:
    db_name = "recipes_schema"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
        

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_register(data):
        is_valid = True # we assume this is true

        if len(data['first_name']) < 3:
            flash('First name must be at least 3 characters.',"register")
            is_valid = False

        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters.","register")
            is_valid = False

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!","register")
            is_valid = False
                        
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.","register")
            is_valid = False
            
        if data['password'] != data['password']:
            flash("Passwords do not match.","register")
            is_valid = False
            
        return is_valid

    @staticmethod
    def validate_login(data):
        
        user = User.get_by_email({'email': data['email']})

        if not user:
            flash("Invalid Email","login")
            return False

        if not bcrypt.check_password_hash(user.password, data['password']):
            flash("Invalid Password","login")
            return False

        return True


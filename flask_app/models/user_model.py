from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt (app)
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db_name = "letterbox"
    
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    #Creates User with validations in place 
    @classmethod
    def create_user(cls, data):
        if not cls.validate_user(data):
            return False
        else:
            data = cls.parse_user_data(data)
        query = """
        INSERT INTO users (first_name, last_name, username, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s)
        ;"""
        user_id = MySQLConnection(cls.db).query_db(query, data)
        session['user_id'] = user_id
        return user_id
    
    #Saves User to database 
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name, username, email,password) VALUES(%(first_name)s,%(last_name)s, %(username)s, %(email)s,%(password)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    #Get all from users 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users
    
    
    #Get user by email
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    
    #Get user by id 
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) >= 1: 
            return cls(results[0]) 
        else: 
            users = [] 
    
    #Validation for register
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['username']) < 3:
            flash("Username must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 5:
            flash("Password must be at least 5 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
            is_valid= False
        return is_valid
    
    @staticmethod
    def parse_user_data(data):
        parsed_data = {
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'username' : data['username'],
            'email' : data['email'],
            'password' : bcrypt.generate_password_hash(data['password'])
        }
        return parsed_data
   
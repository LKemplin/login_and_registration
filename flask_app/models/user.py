from flask_app.config.mysqlconnection import connectToMySQL
from flask import request, flash
import re
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db = "log_and_reg"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["last_name"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_user(user):
        is_valid = True
        if user["first_name"].isalpha() == False:
            flash("Name fields must be letters only.")
            is_valid = False
        if len(user["first_name"]) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if user["last_name"].isalpha() == False:
            flash("Name fields must be letters only.")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email address")
            is_valid = False
        if request.form["password"] != request.form["confirm_password"]:
            flash("Passwords do not match.")
            is_valid = False
        return is_valid

    @classmethod
    def register(cls, data):
        query = "INSERT INTO login_info (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)
        

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM login_info WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        this_user = cls(results[0])
        return this_user

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM login_info WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        this_user = cls(results[0])
        return this_user
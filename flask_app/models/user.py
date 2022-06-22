from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
            self.id = data['id']
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.email = data['email']
            self.password = data['password']
            self.created_at = data['created_at']
            self.updated_at = data['updated_at']


    @classmethod
    def get_one(cls, data):
        query = "SELECT * "
        query += "FROM users "
        query += "WHERE email=%(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) >0:
            return cls(result[0])
        else:
            return None


    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) "
        query += "VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result


    @staticmethod
    def validate_login(data):
        isValid = True
        if data ['email'] == "":
            flash("Please enter your Email.", "error_email")
            isValid = False
        if data ['password'] == "":
            flash("Please enter your Password.", "error_password")
            isValid = False
        return isValid


    @staticmethod
    def validate_session():
        if "id" in session:
            return True
        else:
            flash("Sorry pal, you must be logged in to see this content :/ ", "error_login")
            return False


    @staticmethod
    def validate_registration(data):
        isValid = True
        if data ['first_name'] == "":
            flash("Please enter your First Name.", "error_register_first_name")
            isValid = False

        if data ['last_name'] == "":
            flash("Please enter your Last Name.", "error_register_last_name")
            isValid = False

        if data ['email'] == "":
            flash("Please enter your Email.", "error_register_email")
            isValid = False

        if data ['password'] == "":
            flash("Please enter your Password.", "error_register_password")
            isValid = False

        if data ['password_confirmation'] != data['password']:
            flash("Your passwords dont match, please try again.", "error_register_password_confirmation")
            isValid = False

        if len(data['password']) < 8:
            flash("Passwords must be at least 8 characters long.", "error_register_password")
            isValid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Please enter a valid email.", "error_register_email")
            isValid = False
        return isValid
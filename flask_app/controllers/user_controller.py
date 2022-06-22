from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user import User
# from flask_app.models."class" import Dojo     (no quotes)
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
@app.route("/login")
def display_login():
    if User.validate_session() == True:
        return redirect("/dashboard")
    else:
        return render_template("login_registration.html")

@app.route("/login", methods=['POST'])
def user_login():
    if User.validate_login(request.form) == False:
        return redirect("/login")
    else:
        print(request.form)
        result = User.get_one(request.form)


        if result == None:
            flash("Wrong credentials", "error_login")
            return redirect("/login")
        else:
            if not bcrypt.check_password_hash(result.password, request.form['password']):
                flash("Wrong credentials", "error_login")
                return redirect("/login")
            else:
                session['first_name'] = result.first_name
                session['last_name'] = result.last_name
                session['email'] = result.email
                session['id'] = result.id
                return redirect("/dashboard")


@app.route("/logout", methods = ['POST'])
def user_logout():
    session.clear()
    return redirect("/login")


@app.route("/dashboard")
def dash():
    if User.validate_session() == False:
        return redirect ("/login")
    else:
        return render_template("dashboard.html")


@app.route("/user/new", methods = ['POST'])
def create():
    if User.validate_registration(request.form) == False:
        return redirect("/login")
    else:
        if User.get_one({ "email" : request.form['email'] }) == None:
            data = {
                "first_name" : request.form['first_name'],
                "last_name" : request.form['last_name'],
                "email" : request.form['email'],
                "password" : bcrypt.generate_password_hash(request.form['password'])
            }
            user_id = User.create(data)
            session['first_name'] = request.form['first_name']
            session['last_name'] = request.form['last_name']
            session['email'] = request.form['email']
            session['id'] = user_id
            return redirect ("/dashboard")
        else:
            flash("This email is already in use", "error_register_email")
            return redirect("/login")
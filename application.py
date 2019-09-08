import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from helpers import lookup, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

# Configure application
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Ensure templates are auto_reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# configure cs50 Library to use SQLite database
db = SQL("sqlite:///decaflix1.db")

# index
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login user"""

   # Forget any user_id
    session.clear()

    if request.method == "POST":

        errors = []
        # validate input

        # query database for email
        rows = db.execute(
            "SELECT * FROM users WHERE email = :email", email=request.form.get("email"))

        if not request.form.get("email"):
            errors.append({"msg": "Email field must not be empty"})

        elif not request.form.get("password"):
            errors.append({"msg": "Password field must not be empty"})

        elif len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            errors.append({"msg": "invalid username and/or password"})

        if len(errors) > 0:
            return render_template("login.html", errors=errors, email=request.form.get("email"), password=request.form.get("password"))

        else:
            # validation passed

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            session["username"] = rows[0]["username"]

            # Redirect user to home page
            return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    # forget any user_id
    session.clear()

    # user get to the route via get
    if request.method == "POST":

        """Register user"""
        username = request.form.get("username").casefold()
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")

        # validate input before saving to the database
        errors = []

        # query database for username to know if it already exists
        rows = db.execute(
            "SELECT * FROM users WHERE username = :username", username=username)

        if not username and not email and not password:
            errors.append({"msg": "Please fill in all fields"})

        elif len(rows) > 0:
            errors.append({"msg": "Username already exist"})

        elif not username:
            errors.append({"msg": "Username field must not be empty"})

        elif not email:
            errors.append({"msg": "Email field must not be empty"})

        elif not password:
            errors.append({"msg": "Password must not be empty"})

        elif password != confirm_password:
            errors.append({"msg": "Passwords do not match"})

        if len(errors) > 0:
            return render_template("register.html", errors=errors, username=username, email=email, password=password)

        else:
            # validation passed

            id = db.execute("INSERT INTO users (username, email, password) VALUES(:username, :email, :password)",
                            username=username, email=email, password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))

            # flash('Thanks for registering')

            # Remember which user has logged in
            session["user_id"] = id
            session["username"] = username

            return redirect("/")

    return render_template("register.html")


@app.route("/movie", methods=["GET", "POST"])
def movie():

    if request.method == "POST":
        title = request.form.get("title")
        lookup_title = lookup(title)
        print(lookup_title)

        # return render_template("movieBySearch.html", lookup_title=lookup_title)
        # return render_template("movieBySearch.html")

    return render_template("index.html")


@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

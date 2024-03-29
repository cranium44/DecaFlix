import os

from sql import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from helpers import lookup, login_required, all, lookup_by_id
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

# Configure application
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Ensure templates are auto_reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# configure cs50 Library to use SQLite database
db = SQL("sqlite:///decaflix.db")

# index
@app.route("/")
def index():
    movies = all()
    return render_template("index.html", movies=movies)


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

        elif len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            errors.append({"msg": "invalid username and/or password"})

        if len(errors) > 0:
            return render_template("login.html", errors=errors, email=request.form.get("email"), password=request.form.get("password"))

        else:
            # validation passed

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            session["name"] = rows[0]["name"]

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
        name = request.form.get("name").casefold()
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        # validate input before saving to the database
        errors = []

        # query database for username to know if it already exists
        rows = db.execute(
            "SELECT * FROM users WHERE email = :email", email=email)

        if not name and not email and not password:
            errors.append({"msg": "Please fill in all fields"})

        elif len(rows) > 0:
            errors.append({"msg": "Email already exist"})

        elif not name:
            errors.append({"msg": "Name field must not be empty"})

        elif not email:
            errors.append({"msg": "Email field must not be empty"})

        elif not password:
            errors.append({"msg": "Password must not be empty"})

        elif password != confirm_password:
            errors.append({"msg": "Passwords do not match"})

        if len(errors) > 0:
            return render_template("register.html", errors=errors, name=name, email=email, password=password)

        else:
            # validation passed

            id = db.execute("INSERT INTO users (name, email, hash) VALUES(:name, :email, :hash)",
                            name=name, email=email, hash=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))

            # flash('Thanks for registering')

            # Remember which user has logged in
            session["user_id"] = id
            session["name"] = name

            return redirect("/")

    return render_template("register.html")


@app.route("/movie", methods=["GET", "POST"])
def movie():

    if request.method == "POST":
        title = request.form.get("title")

        lookup_search = lookup(title)
        return render_template("search_list.html", lookup_search=lookup_search)
    if request.method == 'GET':
        return render_template("index.html")


@app.route('/add_movie', methods=['POST'])
def add_movie():
    # data = request.args.get("q")
    data = None
    if request.method == 'POST':
        data = request.get_json()
        id = data["id"]
        title = data["title"]
        rating = data["rating"]
        user_id = session["user_id"]
        db.execute("INSERT INTO collection (id, user_id, title, rating) VALUES (:id, :user_id, :title, :rating)", id = id, user_id=user_id, title=title, rating=rating)
        return redirect("/collection")


@app.route('/collection', methods=['GET'])
def collection():
    if request.method == 'GET':
        user_id = session["user_id"]
        collection = db.execute("SELECT * FROM collection WHERE user_id = :user_id", user_id=user_id)
        print(collection)
        return render_template("collection.html",collection=collection)


@app.route('/single', methods=['GET', 'POST'])
@login_required
def method_name():
    if request.method == "GET":
        id = request.args.get('id')
        print(id)
    #    id  = data['id']
        lookup_title = lookup_by_id(id)
        return render_template("single.html", lookup_title=lookup_title)

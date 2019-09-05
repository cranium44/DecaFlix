import requests
import flask.sessions
import flask
import mysql.connector

from tempfile import mkdtemp
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import all, apology, login_required
from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#database connection
con = mysql.connector.connect(
   host = "localhost",
   user = "root",
   password = "",
   database = "decaflix",
   port = 3306
)

db = con.cursor()

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

@app.route('/')
def index():
   api =""
   catalogue = all()
   return render_template("index.html", catalogue=catalogue) #

@app.route('/login', methods=['GET','POST'])
def login():
   #clear session
   #session.clear()
   if request.method == "POST":
      #retrieve info from the page
      username = requests.form.get("username")
      password = requests.form.get("password")
      hashed  = generate_password_hash(password)
      db.execute("select * from databas where username = :username", username)
      res = db.fetchall()
      if res[0]['hash'] == hash:
         session['id'] == res[0]['user_id']
         return redirect('/')
      elif res is None:
         return apology("The user does not exist")
      else:
         return apology("Username and/or password incorrect")

   if request.method == "GET":
      return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == 'GET':
      return render_template("register.html")

   if request.method == "POST":
      #forget present user
      session.clear()

      #retrieve information from the form
      username = request.form.get("username")
      password = request.form.get("password")
      confirmation = request.form.get("confirmation")

      #check username availability
      isAvailable = user_available(username)

      #run query and add the new user given that the usename exists and passwords match
      if isAvailable:
         if password == confirmation:
            db.execute("INSERT INTO users(username, hash) VALUES(:username, :hash)", username, generate_password_hash(password))
            db.execute("SELECT user_id FROM users WHERE username = :username", username)
            res = db.fetchall()
            session['user_id'] = res[0]['user_id'] #remember current user
            return render_template("index.html")
         else:
            return apology("Passwords do not match")
      else:
         return apology("Username not available")



@app.route('/collection', methods=['GET', 'POST'])
@login_required
def method_name():
   if request.method == 'GET':
      pass
import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from helpers import lookup

# Configure application
app = Flask(__name__)

# Ensure templates are auto_reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#index
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # forget any user_id
    # session.clear()

    # user get to the route via get
    if request.method == "GET":
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # user get to the route via get
    if request.method == "GET":
        return render_template("login.html")


@app.route("/movie", methods=["GET", "POST"])
def movie():

    if request.method == "POST":
        title = request.form.get("title")

        lookup_title = lookup(title)
        return render_template("single.html", lookup_title=lookup_title)

    return render_template("index.html")

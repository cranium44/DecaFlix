import requests
import flask.sessions
import flask
import mysql.connector

from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import lookup
from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

con = mysql.connector.connect(
   host = "localhost",
   user = "root",
   password = "",
   database = "decaflix",
   port = 3306
)

db = con.cursor()

@app.route('/login', methods=['GET','POST'])
def login():
   #clear session
   session.clear()

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


@app.route('/register', methods=['GET', 'POST'])
def register():
   if requests.method == "POST":
      username = requests.form.get("username")
      password = requests.form.get("password")
      confirmation = requests.form.get("confirmation")

      #check username availability
      isAvailable = user_available(username)
      if isAvailable:
         if password == confirmation:
            db.execute("INSERT INTO users(username, hash) VALUES(:username, :hash)", username, generate_password_hash(password))
            db.execute("SELECT user_id FROM users WHERE username = :username", username)
            res = db.fetchall()
            session['user_id'] = res[0]['user_id']
         else:
            return apology("Passwords do not match")
      else:
         return apology("Username not available")


@app.route('/', methods=['GET', 'POST'])
def index():
   api =""
   catalogue = lookup(api)
   return render_template("index.html", catalogue)

@app.route('/collection', methods=['GET', 'POST'])
def method_name():
   pass

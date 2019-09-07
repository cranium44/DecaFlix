import os
import flask
# import mysql.connector

from flask_session.__init__ import Session
from sql import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from tempfile import mkdtemp
#from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import all, apology, login_required, lookup, user_available


app = Flask(__name__)
# app.secret_key = 'axaaxxxa'
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


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


db = SQL("sqlite:///decaflix.db")

@app.route('/')
def index():
   api =""
   catalogue = all()
   return render_template("index.html", catalogue=catalogue) #



@app.route('/login', methods=['GET','POST'])
def login():
   #clear session
   session.clear()
   if request.method == "POST":
      #retrieve info from the page
      email = request.form.get("email")
      password = request.form.get("password")
      #hash  = generate_password_hash(password)
      print(hash)
      res = db.execute("SELECT id, hash FROM users WHERE email = :email", email=email)
      print(res)
      if check_password_hash(res[0]['hash'], password):
         session["user_id"] == res[0]['id']
         return redirect('/')
      elif res[0] == []:
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
      
      #retrieve information from the form
      name = request.form.get("name")
      email = request.form.get("email")
      password = request.form.get("password")
      confirmation = request.form.get("confirmation")

      #check username availability
      isAvailable = user_available(email)

      #run query and add the new user given that the usename exists and passwords match
      if isAvailable:
         if password == confirmation:
            db.execute("INSERT INTO users(name, email, hash) VALUES(:name, :email, :hash)", name=name, email=email, hash = generate_password_hash(password))
            res = db.execute("SELECT id FROM users WHERE email = :email", email=email)
            #session['id'] = res[0]['id'] #remember current user
            return render_template("index.html")
         else:
            return apology("Passwords do not match")
      else:
         return apology("Username not available")



@app.route('/collection', methods=['GET', 'POST'])
#@login_required
def method_name():
   if request.method == 'GET':
      pass


@app.route("/movie", methods=["GET", "POST"])
def movie():

    if request.method == "POST":
        title = request.form.get("title")

        lookup_title = lookup(title)
        return render_template("single.html", lookup_title=lookup_title)

    return render_template("index.html")

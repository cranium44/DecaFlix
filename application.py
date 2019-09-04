import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from helpers import lookup

# Configure application
app = Flask(__name__)

# Ensure templates are auto_reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


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

        look_up_title = lookup(title)
        print(look_up_title)

    return "good"

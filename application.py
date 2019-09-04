import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

# Configure application
app = Flask(__name__)

# Ensure templates are auto_reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # user get to the route via get
    if request.method == "GET":
        return render_template("register.html")

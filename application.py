import pip._vendor.requests
import flask.sessions
import flask
import mysql.connector
from cs50 import SQL
con = mysql.connector.connect()
db = SQL("http//:localhost/decaflix")

@app.route('/login')
def login():
   username = requests.form.get("username")
   pasword = requests.form.get("password")
   hashed  = genera

@app.route('/register', methods=['GET', 'POST'])
def register():
   pass

@app.route('/', methods=['GET', 'POST'])
def method_name():
   pass
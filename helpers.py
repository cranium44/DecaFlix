import pip._vendor.requests
import mysql.connector

con = mysql.connector.connect(
   host = "localhost",
   user = "root",
   password = "",
   database = "decaflix",
   port = 3306
)

db = con.cursor()

def lookup(title):
    pass

def apology(message):
    pass



def user_available(username):
    isAvailable = False
    res = con.execute(
        "select * from users where username = :username", username)
    if res is None:
        isAvailable = True
    return isAvailable

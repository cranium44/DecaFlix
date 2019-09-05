import requests
import mysql.connector
import json
import http.client

con = mysql.connector.connect(
   host = "localhost",
   user = "root",
   password = "",
   database = "decaflix",
   port = 3306
)

db = con.cursor()

def all():
# https://api.themoviedb.org/3/movie/550?api_key=28dda9f76d76f128b47831768bc9a103    COMPLETE_API = ""

    conn = http.client.HTTPSConnection("api.themoviedb.org")
    payload = "{}"
    conn.request("GET", "/3/movie/%7Bmovie_id%7D?language=en-US&api_key=28dda9f76d76f128b47831768bc9a103%3C%3Capi_key%3E%3E", payload)
    res = conn.getresponse()
    data = res.read()
    return data

def apology(message):
    return render_template("apology.html", message)



def user_available(username):
    isAvailable = False
    res = con.execute(
        "select * from users where username = :username", username)
    if res is None:
        isAvailable = True
    return isAvailable

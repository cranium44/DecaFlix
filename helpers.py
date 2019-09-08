import os
import json
import http.client
import requests
from functools import wraps
from flask import redirect, render_template, request, session
# import urllib.parse
# from sql import SQL


# db = SQL("sqlite:///decaflix.db")


def login_required(f):
    """Decorate routes to require login"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def all():
    # https://api.themoviedb.org/3/movie/550?api_key=28dda9f76d76f128b47831768bc9a103

    conn = http.client.HTTPSConnection("api.themoviedb.org")
    payload = "{}"
    conn.request(
        "GET", "/3/discover/movie?sort_by=popularity.desc&api_key=28dda9f76d76f128b47831768bc9a103", payload)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return data


def apology(message):
    return render_template("apology.html", message=message)


def lookup(title):
    """Look up title for movie"""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(
            f"http://www.omdbapi.com/?s={title}&apikey=ced7be9a")  # http://www.omdbapi.com/?s=Batman&apikey=ced7be9a
        response.raise_for_status()
    except requests.RequestException:
        return None

    # parse response
    try:
        movie = response.json()
        return {
            "search": movie["Search"],
            # "year": movie["Year"],
            # "rated": movie["Rated"],
            # "released": movie["Released"],
            # "runtime": movie["Runtime"],
            # "genre": movie["Genre"],
            # "director": movie["Director"],
            # "writer": movie["Writer"],
            # "actors": movie["Actors"],
            # "plot": movie["Plot"],
            # "language": movie["Language"],
            # "poster": movie["Poster"],
            # "imdbRating": movie["imdbRating"],
            # "imdbID": movie["imdbID"],
            # "DVD": movie["DVD"],
            # "boxOffice": movie["BoxOffice"],
            # "production": movie["Production"],
            # "website": movie["Website"],

        }

    except (KeyError, TypeError, ValueError):
        return None


# import pip._vendor.requests
# import mysql.connector

# con = mysql.connector.connect(
#     host='localhost', database='decaflix', user='root', password='')


# def lookup(title):
#     pass


# def user_available(email):
#     isAvailable = False
#     res = db.execute("SELECT * FROM users WHERE email = :email", email=email)
#     print(res)
#     if res[0] == []:
#         isAvailable = True
#     return isAvailable

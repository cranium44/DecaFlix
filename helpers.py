import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def login_required(f):
    """Decorate routes to require login"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(title):
    """Look up title for movie"""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(
            f"http://www.omdbapi.com/?t={title}&apikey=ced7be9a")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # parse response
    try:
        movie = response.json()
        return {
            "title": movie["Title"],
            "year": movie["Year"],
            "rated": movie["Rated"],
            "released": movie["Released"],
            "runtime": movie["Runtime"],
            "genre": movie["Genre"],
            "director": movie["Director"],
            "writer": movie["Writer"],
            "actors": movie["Actors"],
            "plot": movie["Plot"],
            "language": movie["Language"],
            "poster": movie["Poster"],
            "imdbRating": movie["imdbRating"],
            "imdbID": movie["imdbID"],
            "DVD": movie["DVD"],
            "boxOffice": movie["BoxOffice"],
            "production": movie["Production"],
            "website": movie["Website"],

        }

    except (KeyError, TypeError, ValueError):
        return None


# import pip._vendor.requests
# import mysql.connector

# con = mysql.connector.connect(
#     host='localhost', database='decaflix', user='root', password='')


# def lookup(title):
#     pass


# def user_available(username):
#     isAvailable = False
#     res = con.execute(
#         "select * from users where username = :username", username)
#     if res is None:
#         isAvailable = True
#     return isAvailable

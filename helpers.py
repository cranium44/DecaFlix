import os
import json
import http.client
import requests
from functools import wraps
from flask import redirect, render_template, request, session
# import urllib.parse
from sql import SQL


db = SQL("sqlite:///decaflix.db")
base_url = "https://image.tmdb.org/t/p/"
sizes = ["w92", "w154", "w185", "w342", "w500", "w780", "original"]


def login_required(f):
    """Decorate routes to require login"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def all():

    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(
            f"http://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=28dda9f76d76f128b47831768bc9a103")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # parse response
    try:
        movies = response.json()
        popular = movies["results"]
        pop_list = []
        for i in range(len(popular)):
            pop = {"popularity": popular[i]["popularity"],
                   "poster_path": base_url + sizes[3] + popular[i]["poster_path"],
                   "id": popular[i]["id"],
                   "title": popular[i]["title"],
                   "overview": popular[i]["overview"],
                   "rating": popular[i]["vote_average"],
                   "date": popular[i]["release_date"]}
            pop_list.append(pop)
        return pop_list
    except (KeyError, TypeError, ValueError):
        return None


def apology(message):

    return render_template("apology.html", message=message)


def lookup(title):
    """Look up title for movie"""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(
            f"http://www.omdbapi.com/?s={title}&apikey=ced7be9a")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # parse response
    try:
        movie = response.json()
        search = movie["Search"]
        search_list = []
        for i in range(len(search)):
            search_prop = {"title": search[i]["Title"],
                            "year": search[i]["Year"], 
                            "poster": search[i]["Poster"],
                            "id": search[i]["imdbID"]}
            search_list.append(search_prop)

        return search_list

    except (KeyError, TypeError, ValueError):
        return None


def lookup_by_id(i_d):
    """Look up id for movie"""

    # Contact API
    try:
        response = requests.get(
            f"http://www.omdbapi.com/?i={i_d}&apikey=ced7be9a")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # parse response
    try:
        movie = response.json()
        return {
            "title":movie["Title"],
            "id":movie["imdbID"],
            "plot":movie["Plot"],
            "year":movie["Year"],
            "poster":movie["Poster"],
            "gross":movie["BoxOffice"],
            "rating":movie["imdbRating"],
            "website":movie["Website"],
            "director":movie["Director"],
            "writer":movie["Writer"],
            "genre":movie["Genre"],
            "actors":movie["Actors"]
        }

    except (KeyError, TypeError, ValueError):
        return None
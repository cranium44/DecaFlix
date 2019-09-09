import os
import json
import http.client
import requests
from functools import wraps
from flask import redirect, render_template, request, session
# import urllib.parse
# from sql import SQL


db = SQL("sqlite:///decaflix.db")
base_url = "https://image.tmdb.org/t/p/"
sizes = ["w92","w154","w185","w342","w500","w780","original"]


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
                   "poster_path": popular[i]["poster_path"],
                   "id": popular[i]["id"],
                   "title": popular[i]["title"],
                   "overview": popular[i]["overview"],
                   "rating": popular[i]["vote_average"],
                   "date": popular[i]["release_date"]}
            pop_list.append(pop)
        return pop_list


    except (KeyError, TypeError, ValueError):
        return None
    # try:
    #     api_key = os.environ.get("API_KEY")
    #     response = requests.get(
    #         f"api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=28dda9f76d76f128b47831768bc9a103")
    #     response.raise_for_status()
    # except requests.RequestException:
    #     return None

    # try:
    #     all_movie = response.json()
    #     return all_movie

    # except (KeyError, TypeError, ValueError):
    #     return None


def apology(message):

    return render_template("apology.html", message=message)


def lookup(title):
    """Look up title for movie"""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(
            f"http://www.omdbapi.com/?t={title}&apikey=ced7be9a")  # http://www.omdbapi.com/?s=Batman&apikey=ced7be9a
        response.raise_for_status()
    except requests.RequestException:
        return None

    # parse response
    try:
        movie = response.json()
        return {
            # "search": movie["Search"],
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

# def user_available(email):
#     isAvailable = False
#     res = db.execute("SELECT * FROM users WHERE email = :email", email=email)
#     print(res)
#     if res[0] == []:
#         isAvailable = True
#     return isAvailable

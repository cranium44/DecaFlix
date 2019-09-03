import pip._vendor.requests
import mysql.connector

con = mysql.connector.connect(
    host='localhost', database='decaflix', user='root', password='')


def lookup(title):
    pass


def user_available(username):
    isAvailable = False
    res = con.execute(
        "select * from users where username = :username", username)
    if res is None:
        isAvailable = True
    return isAvailable

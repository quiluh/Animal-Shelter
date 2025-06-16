import pymysql
from flask import Flask, render_template, request, redirect
import random

app = Flask(__name__)

def create_connection():
    return pymysql.connect(
        host="10.0.0.17:3306",
        user="clymesa",
        password="ANGLE",
        db="animal-shelter",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def Home():
    randomIndexes = []
    rows,columns = (1,3)
    randomDogs = [[None for i in range(columns)] for o in range(rows)]
    
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * from dogs")
            result = list(cursor.fetchall())
            while len(randomIndexes) != rows*columns:
                index = random.randint(0,len(result)-1)
                if index not in randomIndexes:
                    randomIndexes.append(index)

    randomIndexes = iter(randomIndexes)
    for i in randomDogs:
        for index in range(len(i)):
            i[index] = result[next(randomIndexes)]

    return render_template("index.html",randomDogs=randomDogs)

app.run(debug=True)
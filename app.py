import pymysql
from flask import Flask, render_template, request, redirect
import random
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

def create_connection():
    return pymysql.connect(
        host="10.0.0.17",
        user="clymesa",
        password="ANGLE",
        db="clymesa_animal-shelter",
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

@app.route("/viewDog")
def ViewDog():
    id = request.args["id"]
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM dogs WHERE id = %s"
            values = (id)
            cursor.execute(sql, values)
            result = cursor.fetchone()
    return render_template("viewDog.html",dog=result)

def saveFile(file):
    file.save(f"static/uploads/{file.name}")
    return f"/static/uploads/{file.name}"

@app.route("/addDog",methods=["GET","POST"])
def AddDog():
    if request.method == "GET":
        return render_template("addDog.html")
    elif request.method == "POST":
        name = request.form["name"]
        info = request.form["info"]
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = """INSERT INTO dogs (name,info) VALUES (%s,%s)"""
                values = (name,info)
                cursor.execute(sql,values)
                connection.commit()
        return render_template("index.html")

app.run(debug=True)
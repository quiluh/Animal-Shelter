import pymysql
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

def create_connection():
    return pymysql.connect(
        host="10.0.0.17:3306",
        user="clymesa",
        password="ANGLE",
        db="animal-shelter"
    )

app.run(debug=True)
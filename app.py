#!flask/bin/python
from os import environ
from flask import Flask, render_template
from src.sdk.students import StudentController
from src.config import conn

app = Flask(__name__, static_folder="templates", static_url_path="")


@app.route("/")
def output():
    # serve index template
    return render_template("index.html")

@app.route("/alunos")
def alunos():
    StudentController(conn).create("my_student")
    return 'OK'


if __name__ == "__main__":
    # run!
    from waitress import serve

    port = int(environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)

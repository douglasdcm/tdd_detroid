#!flask/bin/python
from os import environ
from flask import Flask, render_template, request
from src.sdk.students import StudentController
from src.sdk.courses import CourseController
from src.config import conn_internal
from json import dumps
from src.utils.exceptions import ErroAluno, ErrorCourse

app = Flask(__name__, static_folder="templates", static_url_path="")
SUCCESS = dumps({"status": "ok", "message": "success"})


def __failed(e, detail=False):
    fail = {"status": "failed", "message": None}
    if detail:
        fail["message"] = str(e)
        return dumps(fail)
    fail["message"] = e
    return dumps(fail)


@app.route("/")
def output():
    # serve index template
    return render_template("index.html")


@app.route("/course", methods=["POST"])
def course():
    try:
        name = request.json["name"]
        CourseController(conn_internal).create(name)
        return SUCCESS
    except (ErrorCourse, ErroAluno) as e:
        return __failed(e, detail=True)
    except Exception as e:
        return __failed(e)


@app.route("/student", methods=["POST"])
def student():
    try:
        name = request.json["name"]
        StudentController(conn_internal).create(name)
        return SUCCESS
    except (ErrorCourse, ErroAluno) as e:
        return __failed(e, detail=True)
    except Exception as e:
        return __failed(e)


if __name__ == "__main__":
    # run!
    from waitress import serve

    port = int(environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)

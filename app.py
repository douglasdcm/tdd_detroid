#!flask/bin/python
from os import environ
from flask import Flask, render_template, request
from src.controllers import courses, students, disciplines
from json import dumps
from src.utils.exceptions import ErrorStudent, ErrorCourse, ErrorDiscipline
import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='application.log', level=logging.ERROR,
                    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__, static_folder="templates", static_url_path="")
SUCCESS = dumps({"status": "ok", "message": "success"})


def __failed(e, detail=True):
    fail = {"status": "failed", "message": None}
    if detail:
        fail["message"] = str(e)
        return dumps(fail)
    fail["message"] = e
    logging.error(str(e))
    return dumps(fail)


@app.route("/")
def output():
    # serve index template
    return render_template("index.html")


@app.route("/course", methods=["POST"])
def course():
    try:
        name = request.json["name"]
        courses.create(name)
        return SUCCESS
    except (ErrorCourse, ErrorStudent) as e:
        return __failed(e, detail=True)
    except Exception as e:
        return __failed(e)

@app.route("/discipline", methods=["POST"])
def discipline():
    try:
        name = request.json["name"]
        course_id = request.json["course_id"]
        disciplines.create(name, course_id)
        return SUCCESS
    except (ErrorCourse, ErrorDiscipline) as e:
        return __failed(e)
    except Exception as e:
        return __failed(e)

@app.route("/subscription-discipline", methods=["POST"])
def subscription_discipline():
    try:
        student_id = request.json["student_id"]
        discipline_id = request.json["discipline_id"]
        students.subscribe_in_discipline(student_id, discipline_id)
        return SUCCESS
    except (ErrorStudent) as e:
        return __failed(e)
    except Exception as e:
        return __failed(e)

@app.route("/subscription-course", methods=["POST"])
def subscription_course():
    try:
        student_id = request.json["student_id"]
        course_id = request.json["course_id"]
        students.subscribe_in_course(student_id, course_id)
        return SUCCESS
    except (ErrorStudent) as e:
        return __failed(e)
    except Exception as e:
        return __failed(e)

@app.route("/student", methods=["POST"])
def student():
    try:
        name = request.json["name"]
        students.create(name)
        return SUCCESS
    except (ErrorCourse, ErrorStudent) as e:
        return __failed(e)
    except Exception as e:
        logging.error(str(e))
        return __failed(e)


if __name__ == "__main__":
    # run!
    from waitress import serve

    port = int(environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)

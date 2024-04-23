from flask import Flask
from src import cli_helper
from src.database import Database

app = Flask(__name__)


@app.route("/")
def root():
    return f"Home"


@app.route("/list-courses")
def list_courses():
    result = cli_helper.list_all_course_details(Database())
    return f"{result}"


@app.route("/create-course")
def create_course():
    try:
        result = cli_helper.create_course(Database(), "my-course3", 10)
        return f"{result}"
    except Exception as e:
        print(str(e))

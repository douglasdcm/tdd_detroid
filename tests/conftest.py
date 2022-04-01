from pytest import fixture
from src.libs.database import Database
from sqlite3 import connect
from src.model.university import University
from src.model.course import Course
from src.model.discipline import Discipline


@fixture
def setup_database_in_memory():
    db = Database(connect(":memory:"))
    db.create_table("students", "score")
    db.create_table("disciplines", "grade")
    db.create_table("university", "status, course_id")
    yield
    db.delete_table("students")
    db.delete_table("disciplines")
    db.delete_table("university")


@fixture
def setup_valid_univertity():
    quantity_courses = quantity_disciplines = 3
    university = University()
    for i in range(quantity_courses):
        course = Course()
        course.set_id(i + 1)
        for j in range(quantity_disciplines):
            course.add_discipline(Discipline())
        university.add_course(course)
    university.create()
    yield university

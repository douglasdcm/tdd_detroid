from src.utils import sql_client
from src.schemes.course import CourseDB
from src.utils.exceptions import ErrorCourse
from pytest import raises, mark
from src.controllers import courses


def test_course_pega_id():
    courses.create(name="any")
    assert 1 == len(sql_client.get_all(CourseDB))


def test_course_create():
    courses.create(name="any")
    assert sql_client.get(CourseDB, 1).name == "any"


@mark.parametrize("input", [(""), ("  ")])
def test_name_course_nao_vazio(input):
    with raises(ErrorCourse, match="name do course invalido"):
        courses.create(input)


def test_nao_create_course_com_mesmo_name():
    courses.create("any")
    with raises(ErrorCourse, match="Existe outro course com o name any"):
        courses.create("any")

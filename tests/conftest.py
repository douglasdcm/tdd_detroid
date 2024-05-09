import pytest
from src import database


@pytest.fixture(autouse=True, scope="function")
def set_in_memory_database():
    db = database.Database(":memory:")
    db = set_database_for_tests(db)
    yield db


def set_database_for_tests(db):

    # TODO need to check if the courses are available
    db.enrollment.populate("douglas", "098.765.432.12", "adm")
    db.enrollment.populate("maria", "028.745.462.18", "mat")
    db.enrollment.populate("joana", "038.745.452.19", "port")
    db.enrollment.populate("any", "123.456.789-10", "any")
    db.enrollment.populate("other", "123.456.789-10", "any")
    db.enrollment.populate("another", "123.456.789-10", "any")

    db.course.populate("adm", subjects="")
    db.course.populate("mat")
    db.course.populate("port")
    db.course.populate("any")
    db.course.populate("noise")
    db.course.populate("deact")
    db.course.populate("act")
    db.course.populate("nosubjects", state="", subjects="")

    db.subject.populate("any", "any1")  # e4c858cd917f518194c9d93c9d13def8
    db.subject.populate("any", "any2")  # 283631d2292c54879b9aa72e27a1b4ff
    db.subject.populate("any", "any3")  # 0eaaeb1a39ed5d04a62b31cd951f34ce
    db.subject.populate(
        "course1", "subject_full", 0
    )  # ef15a071407953bd858cfca59ad99056
    db.subject.populate(
        "course1", "subject_removed", 0, "removed"
    )  # ef15a071407953bd858cfca59ad99056

    db.semester.populate("2023-2", "closed")
    db.semester.populate("2024-1", "open")
    db.semester.populate("1234-1", "open")
    db.semester.populate("1234-2", "open")
    db.semester.populate("1234-3", "open")
    db.semester.populate("1234-4", "open")
    db.semester.populate("1234-5", "open")
    db.semester.populate("1234-6", "open")
    db.semester.populate("1234-7", "open")
    db.semester.populate("1234-8", "open")
    db.semester.populate("1234-9", "open")
    db.semester.populate("1234-10", "open")
    db.semester.populate("1234-11", "open")
    return db

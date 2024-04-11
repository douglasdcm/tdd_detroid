import pytest
from src.services.subject_handler import SubjectHandler, NonValidSubject
from src import database as db
from src.utils import generate_subject_identifier


def test_remove_invalid_subject_return_error():
    database = db.Database()
    subject_handler = SubjectHandler(database)

    with pytest.raises(NonValidSubject):
        subject_handler.remove()


def test_remove():
    database = db.Database()
    subject_handler = SubjectHandler(database)
    subject_handler.load_from_database(generate_subject_identifier("any", "any1"))
    assert subject_handler.remove() == "removed"


def test_activate_removed_subject_return_error():
    database = db.Database()
    subject_handler = SubjectHandler(
        database, generate_subject_identifier("any", "any1")
    )
    subject_handler.activate()
    subject_handler.remove()

    with pytest.raises(NonValidSubject):
        subject_handler.activate()


def test_activate_invalid_subject_return_error():
    database = db.Database()
    subject_handler = SubjectHandler(database)
    subject_handler.load_from_database(
        generate_subject_identifier("course1", "subject_removed")
    )

    with pytest.raises(NonValidSubject):
        subject_handler.activate()


def test_activate():
    database = db.Database()
    subject_handler = SubjectHandler(database)
    subject_handler.name = "any"

    assert subject_handler.activate() == "active"

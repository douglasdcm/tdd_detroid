import pytest
from src.services.subject_handler import SubjectHandler, NonValidSubject
from src import mocks
from src import database as db


@pytest.fixture(autouse=True)
def restart_database():
    mocks.SUBJECT_STATE = "active"


def test_remove_invalid_subject_return_error():
    database = mocks.Database()
    subject_handler = SubjectHandler(database)

    with pytest.raises(NonValidSubject):
        subject_handler.remove()


def test_remove():
    database = db.Database()
    subject_handler = SubjectHandler(database)
    subject_handler.load_from_database("e4c858cd917f518194c9d93c9d13def8")
    assert subject_handler.remove() == "removed"


def test_activate_removed_subject_return_error():
    database = db.Database()
    subject_handler = SubjectHandler(database, "f65774a5f48d55768dfefac51136724e")
    subject_handler.activate()
    subject_handler.remove()
    mocks.SUBJECT_STATE = "removed"

    with pytest.raises(NonValidSubject):
        subject_handler.activate()


def test_activate_invalid_subject_return_error():
    database = mocks.Database()
    subject_handler = SubjectHandler(database)

    with pytest.raises(NonValidSubject):
        subject_handler.activate()


def test_activate():
    database = db.Database()
    subject_handler = SubjectHandler(database)
    subject_handler.name = "any"

    assert subject_handler.activate() == "active"

import pytest
from src.services.subject_handler import SubjectHandler, NonValidSubject
from src import mocks


def test_remove_invalid_subject_return_error():
    database = mocks.Database()
    subject_handler = SubjectHandler(database)

    with pytest.raises(NonValidSubject):
        subject_handler.remove()


def test_remove():
    database = mocks.Database()
    subject_handler = SubjectHandler(database)
    subject_handler.name = "any"
    assert subject_handler.remove() == "removed"


def test_activate_removed_subject_return_error():
    database = mocks.Database()
    subject_handler = SubjectHandler(database)
    subject_handler.name = "any"
    subject_handler.remove()

    with pytest.raises(NonValidSubject):
        subject_handler.activate()


def test_activate_invalid_subject_return_error():
    database = mocks.Database()
    subject_handler = SubjectHandler(database)

    with pytest.raises(NonValidSubject):
        subject_handler.activate()


def test_activate():
    database = mocks.Database()
    subject_handler = SubjectHandler(database)
    subject_handler.name = "any"

    assert subject_handler.activate() == "active"

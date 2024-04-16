import pytest
from src.services.subject_handler import SubjectHandler, NonValidSubject
from src import utils


def test_remove_invalid_subject_return_error(set_in_memory_database):
    subject_handler = SubjectHandler(set_in_memory_database)

    with pytest.raises(NonValidSubject):
        subject_handler.remove()


def test_remove(set_in_memory_database):
    subject_handler = SubjectHandler(set_in_memory_database, course="any")
    subject_handler.name = "any1"
    assert subject_handler.remove() == "removed"


def test_activate_removed_subject_return_error(set_in_memory_database):
    subject_handler = SubjectHandler(
        set_in_memory_database, utils.generate_subject_identifier("any", "any1")
    )
    subject_handler.activate()
    subject_handler.remove()

    with pytest.raises(NonValidSubject):
        subject_handler.activate()


def test_activate_invalid_subject_return_error(set_in_memory_database):
    subject_handler = SubjectHandler(set_in_memory_database)
    subject_handler.load_from_database(
        utils.generate_subject_identifier("course1", "subject_removed")
    )

    with pytest.raises(NonValidSubject):
        subject_handler.activate()


def test_activate(set_in_memory_database):
    subject_identifier = utils.generate_subject_identifier("any", "any1")
    subject_handler = SubjectHandler(set_in_memory_database, subject_identifier)

    assert subject_handler.activate() == "active"

import logging
from src import utils
from src.constants import DUMMY_IDENTIFIER
from src.database import Database
from src.exceptions import NonValidSubject


class SubjectHandler:

    REMOVED = "removed"
    ACTIVE = "active"

    def __init__(
        self, database: Database, identifier=DUMMY_IDENTIFIER, course=None
    ) -> None:
        self.__database = database
        self.__identifier = identifier
        if identifier != DUMMY_IDENTIFIER:
            self.load_from_database(identifier)
        self.__state = None
        self.__enrolled_students = []
        self.__course = course
        self.__max_enrollment = 0
        self.__name = None

    def __check_identifier(self):
        if self.identifier != DUMMY_IDENTIFIER:
            return
        if not self.name:
            raise NonValidSubject("Need to set a name to subject.")
        if not self.course:
            raise NonValidSubject("Need to set a course to subject.")

    def __check_removed(self):
        if self.state == self.REMOVED:
            raise NonValidSubject(
                f"Subject '{self.identifier}' is removed and can not be activated."
            )

    def __generate_identifier_when_subject_ready(self):
        if self.name and self.__course:
            self.__identifier = utils.generate_subject_identifier(
                self.__course,
                self.name,
            )

    def __check_name_leght(self, value):
        if len(value) > 10:
            raise NonValidSubject(
                f"The maximum number of characters to subject's name is '10'."
                f" Set with '{len(value)}'."
            )

    @property
    def identifier(self):
        return self.__identifier

    @property
    def state(self):
        return self.__state

    @property
    def enrolled_students(self):
        return self.__enrolled_students

    @property
    def course(self):
        return self.__course

    @course.setter
    def course(self, value):
        self.__course = value
        self.__generate_identifier_when_subject_ready()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__check_name_leght(value)
        self.__name = value
        self.__generate_identifier_when_subject_ready()

    @property
    def max_enrollment(self):
        return self.__max_enrollment

    @max_enrollment.setter
    def max_enrollment(self, value):
        self.__check_identifier()
        self.load_from_database(self.identifier)
        self.__max_enrollment = value
        self.save()

    def is_available(self):
        return len(self.enrolled_students) < self.__max_enrollment

    def is_active(self):
        return self.__state == self.ACTIVE

    def activate(self):
        self.__check_identifier()
        self.load_from_database(self.identifier)
        self.__check_removed()
        self.__state = self.ACTIVE
        self.save()

        # post condition
        self.__database.subject.load(self.identifier)
        assert self.__database.subject.state == self.ACTIVE
        return self.__state

    def remove(self):
        self.__generate_identifier_when_subject_ready()

        try:
            self.load_from_database(self.identifier)
        except Exception as e:
            logging.error(str(e))
            raise NonValidSubject(
                f"Subject '{self.__name}' not found in course '{self.course}'."
            )

        if not self.state == self.ACTIVE:
            raise NonValidSubject(f"Subject '{self.identifier} is not active.'")

        self.__state = self.REMOVED
        self.save()

        # post condition
        self.__database.subject.load(self.identifier)
        assert self.__database.subject.state == self.REMOVED
        return self.__state

    def save(self):
        self.__database.subject.enrolled_students = ",".join(self.__enrolled_students)
        self.__database.subject.max_enrollment = self.__max_enrollment
        self.__database.subject.state = self.__state
        self.__database.subject.save()

    def add(self):
        self.__database.subject.name = self.name
        self.__database.subject.state = self.state
        self.__database.subject.identifier = self.identifier
        self.__database.subject.enrolled_students = self.__enrolled_students
        self.__database.subject.max_enrollment = self.__max_enrollment
        self.__database.subject.course = self.course
        self.__database.subject.add()

    def load_from_database(self, subject_identifier):
        try:
            self.__database.subject.load(subject_identifier)

            self.__name = self.__database.subject.name
            self.__state = self.__database.subject.state
            self.__identifier = self.__database.subject.identifier
            self.__enrolled_students = self.__database.subject.enrolled_students
            self.__max_enrollment = self.__database.subject.max_enrollment
            self.__course = self.__database.subject.course

        except Exception as e:
            logging.error(str(e))
            identifier = subject_identifier
            if self.__name:
                identifier = self.__name
            raise NonValidSubject(f"Subject '{identifier}' not found.")

import uuid
import datetime
from src import mocks


class SubjectHandler:

    def __init__(self, subject_identifier=None) -> None:
        # TODO get from database
        if subject_identifier:
            self.__identifier = uuid.uuid5(uuid.NAMESPACE_URL, subject_identifier).hex
        else:
            self.__identifier = uuid.uuid5(
                uuid.NAMESPACE_URL, str(datetime.datetime.now())
            )
        self.__state = None
        self.__enrolled_students = []
        self.__course = None
        self.__max_enrollment = 0
        if subject_identifier:
            # TODO get from database
            self.__course = mocks.SUBJECT
            self.__max_enrollment = mocks.SUBJECT_MAX_ENROLL

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

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def max_enrollment(self):
        return self.__max_enrollment

    @max_enrollment.setter
    def max_enrollment(self, value):
        self.__max_enrollment = value

    def is_available(self):
        return len(self.enrolled_students) < self.__max_enrollment

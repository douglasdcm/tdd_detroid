import uuid
import datetime


class CourseHandler:

    def __init__(self, identifier=None) -> None:
        if not identifier:
            self.__identifier = uuid.uuid5(
                uuid.NAMESPACE_URL, str(datetime.datetime.now())
            )
        self.__state = "inactive"  # TODO use enum
        self.__enrolled_students = []
        self.__subjects = []
        self.__max_enrollment = 0

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
    def subjects(self):
        return self.__subjects

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

    def enroll_student(self, student_identifier):
        self.__enrolled_students.append(student_identifier)

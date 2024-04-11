import uuid
import datetime
import logging


class CourseHandler:
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"

    def __init__(self, database, identifier=None) -> None:
        # TODO check necessity of this conditions. It is weird.
        if not identifier:
            self.__identifier = uuid.uuid5(
                uuid.NAMESPACE_URL, str(datetime.datetime.now())
            )
        self.__name = None
        self.__state = self.INACTIVE  # TODO use enum
        self.__enrolled_students = []
        self.__subjects = []
        self.__max_enrollment = 0
        self.__database = database

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

    def save(self):
        self.__database.course.name = self.name
        self.__database.course.state = self.state
        self.__database.course.identifier = self.identifier
        self.__database.course.enrolled_students = self.enrolled_students
        self.__database.course.max_enrollment = self.max_enrollment
        self.__database.course.subjects = self.subjects
        self.__database.course.save()

    def load_from_database(self, name):
        try:
            self.__database.course.load_from_database(name)

            self.name = self.__database.course.name
            self.__state = self.__database.course.state
            self.__identifier = self.__database.course.identifier
            self.__enrolled_students = self.__database.course.enrolled_students
            self.max_enrollment = self.__database.course.max_enrollment
            self.__subjects = self.__database.course.subjects

        except Exception as e:
            logging.error(str(e))
            raise NonValidCourse("Course not found.")

    def enroll_student(self, student_identifier):
        if not self.state == self.ACTIVE:
            raise NonValidCourse("Course is not active.")
        self.__enrolled_students.append(student_identifier)
        return True

    def add_subject(self, subject):
        self.subjects.append(subject)

    def cancel(self):
        if not self.name:
            raise NonValidCourse("No name set to course.")
        self.__state = self.CANCELLED
        self.save()
        return self.__state

    def deactivate(self):
        if not self.name:
            raise NonValidCourse("No name set to course.")

        if self.state == self.ACTIVE:
            self.__state = self.INACTIVE
            self.save()
        return self.__state

    def activate(self):
        if not self.name:
            raise NonValidCourse("No name set to course.")

        MINIMUM = 3
        if not len(self.subjects) >= MINIMUM:
            raise NonValidCourse(
                f"Need '{MINIMUM}' subjects. Set '{len(self.subjects)}'"
            )

        self.__identifier = uuid.uuid5(uuid.NAMESPACE_URL, f"{self.name}")
        self.__state = self.ACTIVE
        self.save()
        return self.__state


class NonValidCourse(Exception):
    pass

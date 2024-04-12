import logging


class SubjectHandler:

    REMOVED = "removed"
    ACTIVE = "active"

    def __init__(self, database, subject_identifier=-1) -> None:
        self.__database = database
        self.__identifier = subject_identifier
        self.__state = None
        self.__enrolled_students = []
        self.__course = None
        self.__max_enrollment = 0
        self.__name = None

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

    def is_active(self):
        return self.__state == self.ACTIVE

    def activate(self):
        if not self.identifier:
            raise NonValidSubject()

        if self.state == self.REMOVED:
            raise NonValidSubject()

        self.__state = self.ACTIVE
        self.save()

        # post condition
        self.__database.subject.load(self.identifier)
        assert self.__database.subject.state == self.ACTIVE
        return self.__state

    def remove(self):
        if not self.state == self.ACTIVE:
            raise NonValidSubject()

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
            raise NonValidSubject("Subject not found.")


class NonValidSubject(Exception):
    pass

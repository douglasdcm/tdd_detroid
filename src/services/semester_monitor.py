import logging
from src.database import Database, NotFoundError
from src.services.student_handler import StudentHandler


class SemesterMonitor:

    def __init__(self, database: Database, identifier) -> None:
        self.__CLOSED = "closed"
        self.__OPEN = "open"
        self.__identifier = identifier  # TODO get next from database
        self.__state = self.__OPEN
        self.__database = database

    @property
    def identifier(self):
        return self.__identifier

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

    def open(self):
        if not self.identifier:
            raise NonValidSemester("Need to set the semester identifier")
        if self.__state == self.__CLOSED:
            raise NonValidOperation(
                f"It is not possible to reopen the closed semester '{self.identifier}'"
            )
        self.__database.semester.load_open()
        if self.identifier != self.__database.semester.identifier:
            raise NonValidOperation(
                f"Trying to open a new semester. Opened semester is not '{self.identifier}'"
            )
        self.__state = self.__OPEN

        self.__database.semester.identifier = self.identifier
        self.__database.semester.state = self.state
        self.__database.semester.save()

        # post condition
        assert self.__state == self.__database.semester.state
        return self.__state

    def close(self):
        if not self.identifier:
            raise NonValidSemester("Need to set the semester identifier.")

        self.__database.semester.identifier = self.identifier
        try:
            self.__database.semester.load_by_identifier()
        except NotFoundError as e:
            logging.error(str(e))
            raise NonValidOperation(f"Semester '{self.identifier}' not found")
        except Exception as e:
            logging.error(str(e))
            raise
        self.__state = self.__CLOSED
        self.__database.semester.state = self.state
        self.__database.semester.save()

        student_handler = StudentHandler(self.__database)
        student_rows = student_handler.search_all()

        for row in student_rows:
            student_handler = StudentHandler(self.__database, row.identifier)
            student_handler.calculate_gpa()
            student_handler.increment_semester()

        return self.__state


class NonValidOperation(Exception):
    pass


class NonValidSemester(Exception):
    pass

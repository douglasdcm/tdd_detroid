import logging
from src.database import Database, NotFoundError
from src.services.student_handler import StudentHandler
from src.services.course_handler import CourseHandler
from src.services.grade_calculator import GradeCalculator
from src.constants import (
    STUDENT_APPROVED,
    STUDENT_FAILED,
    MAX_SEMESTERS_TO_FINISH_COURSE,
)


class SemesterMonitor:

    def __init__(self, database: Database, identifier) -> None:
        self.__CLOSED = "closed"
        self.__OPEN = "open"
        self.__identifier = identifier  # TODO get next from database
        self.__state = self.__OPEN
        self.__database = database

    def __check_identifier(self):
        if not self.identifier:
            raise NonValidSemester("Need to set the semester identifier.")

    def __is_course_completed(self, student_handler, course_handler):
        return (
            set(student_handler.subjects).intersection(course_handler.subjects)
            == set(student_handler.subjects)
            and student_handler.semester_counter > MAX_SEMESTERS_TO_FINISH_COURSE
        )

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
        self.__check_identifier()

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

            course_handler = CourseHandler(self.__database)
            course_handler.load_from_database(student_handler.course)
            course_handler.name = student_handler.course
            if self.__is_course_completed(student_handler, course_handler):
                grade_calculator = GradeCalculator(self.__database)
                if grade_calculator.is_approved(student_handler.identifier):
                    student_handler.state = STUDENT_APPROVED
                else:
                    student_handler.state = STUDENT_FAILED

        return self.__state


class NonValidOperation(Exception):
    pass


class NonValidSemester(Exception):
    pass

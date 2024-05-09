import logging
from src.database import Database, NotFoundError
from src.services.student_handler import StudentHandler, NonValidStudent
from src.services.course_handler import CourseHandler
from src.constants import (
    STUDENT_APPROVED,
    STUDENT_FAILED,
    MAX_SEMESTERS_TO_FINISH_COURSE,
    SUBJECT_FAILED,
    STUDENT_APPROVED,
)
from src.exceptions import NonValidOperation, NonValidSemester


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

    def __is_approved(self, student_identifier):
        self.__database.student.load(student_identifier)
        self.__database.course.load_from_database(self.__database.student.course)

        if not self.__is_student_finished_all_subjects():
            return False

        for row in self.__database.grade_calculator.load_all_by_student_identifier(
            student_identifier
        ):
            if row.subject_situation == SUBJECT_FAILED:
                return False
        return True

    def __is_student_finished_all_subjects(self):
        return len(self.__database.student.subjects) == len(
            self.__database.course.subjects
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

        self.__database.semester.save_state(self.state)

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
        self.__database.semester.save_state(self.state)

        student_handler = StudentHandler(self.__database)
        student_rows = student_handler.search_all()

        for row in student_rows:
            try:
                student_handler = StudentHandler(self.__database, row.identifier)
                student_handler.increment_semester()
                student_handler.gpa

                course_handler = CourseHandler(self.__database)
                course_handler.load_from_database(student_handler.course)
                course_handler.name = student_handler.course
                if self.__is_course_completed(student_handler, course_handler):
                    if self.__is_approved(student_handler.identifier):
                        student_handler.state = STUDENT_APPROVED
                    else:
                        student_handler.state = STUDENT_FAILED
            except NonValidStudent as e:
                logging.error(str(e))
                continue
            except Exception as e:
                logging.error(str(e))
                raise

        return self.__state

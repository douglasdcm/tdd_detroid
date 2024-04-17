import logging
from src.database import Database, NotFoundError
from src.constants import SUBJECT_IN_PROGRESS, SUBJECT_FAILED


class GradeCalculator:
    def __init__(self, database: Database) -> None:
        self.__student_identifier = None
        self.__subject_identifier = None
        self.__grade = None
        self.__rows = None
        self.__subject_situation = SUBJECT_IN_PROGRESS
        self.__database = database

    @property
    def student_identifier(self):
        return self.__student_identifier

    @student_identifier.setter
    def student_identifier(self, value):
        self.__student_identifier = value

    @property
    def subject_identifier(self):
        return self.__subject_identifier

    @subject_identifier.setter
    def subject_identifier(self, value):
        self.__subject_identifier = value

    @property
    def subject_situation(self):
        return self.__subject_situation

    @subject_situation.setter
    def subject_situation(self, value):
        self.__subject_situation = value

    @property
    def grade(self):
        return self.__grade

    @grade.setter
    def grade(self, value):
        self.__grade = value

    def load_from_database(self, student_identifier, subject_identifier):
        self.__database.grade_calculator.load(student_identifier, subject_identifier)
        self.__student_identifier = self.__database.grade_calculator.student_identifier
        self.__subject_identifier = self.__database.grade_calculator.subject_identifier
        self.__grade = self.__database.grade_calculator.grade
        self.__subject_situation = self.__database.grade_calculator.subject_situation

    def search(self, student_identifier, subject_identifier):
        return self.__database.grade_calculator.search(
            student_identifier, subject_identifier
        )

    def search_all(self):
        return self.__database.grade_calculator.search_all()

    def remove(self, student_identifier, subject_identifier):
        return self.__database.grade_calculator.remove(
            student_identifier, subject_identifier
        )

    def add(self, student_identifier, subject_identifier, grade):
        self.__database.grade_calculator.student_identifier = student_identifier
        self.__database.grade_calculator.subject_identifier = subject_identifier
        self.__database.grade_calculator.grade = grade
        self.__database.grade_calculator.subject_situation = self.subject_situation
        self.__database.grade_calculator.add()

    def save(self):
        self.__database.grade_calculator.student_identifier = self.student_identifier
        self.__database.grade_calculator.subject_identifier = self.subject_identifier
        self.__database.grade_calculator.grade = self.grade
        self.__database.grade_calculator.subject_situation = self.subject_situation
        self.__database.grade_calculator.save()

    def is_approved(self, student_identifier):
        try:
            self.__rows = (
                self.__database.grade_calculator.load_all_by_student_identifier(
                    student_identifier
                )
            )
        except NotFoundError as e:
            raise NonValidGradeOperation(
                f"Student '{student_identifier}' not enrolled to any subject."
            )
        except Exception:
            logging.error(str(e))
            raise

        for row in self.__rows:
            if row.subject_situation == SUBJECT_FAILED:
                return False
        return True

    def calculate_gpa_for_student(self, student_identifier):
        try:
            self.__rows = (
                self.__database.grade_calculator.load_all_by_student_identifier(
                    student_identifier
                )
            )
        except NotFoundError as e:
            raise NonValidGradeOperation(
                f"Student '{student_identifier}' not enrolled to any subject."
            )
        except Exception:
            logging.error(str(e))
            raise
        total = 0
        for row in self.__rows:
            total += row.grade

        return round(total / len(self.__rows), 1)


class NonValidGradeOperation(Exception):
    pass

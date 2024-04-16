class GradeCalculator:
    def __init__(self, database) -> None:
        self.__student_identifier = None
        self.__subject_identifier = None
        self.__grade = None
        self.__rows = None
        self.__databse = database

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
    def grade(self):
        return self.__grade

    @grade.setter
    def grade(self, value):
        self.__grade = value

    def load_from_database(self, student_identifier, subject_identifier):
        self.__databse.grade_calculator.load(student_identifier, subject_identifier)
        self.__student_identifier = self.__databse.grade_calculator.student_identifier
        self.__subject_identifier = self.__databse.grade_calculator.subject_identifier
        self.__grade = self.__databse.grade_calculator.grade

    def add(self, student_identifier, subject_identifier, grade):
        self.__databse.grade_calculator.student_identifier = student_identifier
        self.__databse.grade_calculator.subject_identifier = subject_identifier
        self.__databse.grade_calculator.grade = grade
        self.__databse.grade_calculator.add()

    def save(self):
        self.__databse.grade_calculator.student_identifier = self.student_identifier
        self.__databse.grade_calculator.subject_identifier = self.subject_identifier
        self.__databse.grade_calculator.grade = self.grade
        self.__databse.grade_calculator.save()

    def calculate_gpa_for_student(self, student_identifier):
        try:
            self.__rows = (
                self.__databse.grade_calculator.load_all_by_student_identifier(
                    student_identifier
                )
            )
        except Exception:
            raise NonValidGradeOperation(
                f"Student '{student_identifier}' not enrolled to any subject."
            )
        total = 0
        for row in self.__rows:
            total += row.grade

        return round(total / len(self.__rows), 1)


class NonValidGradeOperation(Exception):
    pass

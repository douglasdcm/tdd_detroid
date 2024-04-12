class GradeCalculator:
    row = None

    def __init__(self, database) -> None:
        self.__databse = database

    def load_from_database(self, student_identifier, subject_identifier):
        self.__databse.grade_calculator.load(student_identifier, subject_identifier)
        self.student_identifier = self.__databse.grade_calculator.student_identifier
        self.subject_identifier = self.__databse.grade_calculator.subject_identifier
        self.grade = self.__databse.grade_calculator.grade

    def add(self, student_identifier, subject_identifier, grade):
        self.__databse.grade_calculator.student_identifier = student_identifier
        self.__databse.grade_calculator.subject_identifier = subject_identifier
        self.__databse.grade_calculator.grade = grade
        self.__databse.grade_calculator.add()

    # def calculate_for(self, student_identifier):
    #     student_handler = StudentHandler(self.__databse)
    #     student_handler.load_from_database(student_identifier)
    #     total = 0
    #     for subject in student_handler.subjects:
    #         # get grade
    #         total += subject.grade

    #     return total / len(student_handler.subjects)

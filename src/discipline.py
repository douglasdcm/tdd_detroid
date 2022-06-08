class Discipline:

    def __init__(self):
        self.__enrollments = []

    def set_enrollment(self, student):
        self.__enrollments.append(student)

    def get_enrollments(self):
        return self.__enrollments

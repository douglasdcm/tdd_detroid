from src.context import students


class Student:
    def __init__(self) -> None:
        self.__grade = 0
        self.__count_course = 0
        self.__id = len(students)

    def __repr__(self) -> str:
        return f"id {self.__id}"

    def __set_grade(self, grade):
        total = self.__grade
        total += grade
        avg = total / self.__count_course
        self.__grade = avg

    def grade_course(self, grade):
        self.__count_course += 1
        self.__set_grade(grade)

    def get_grade(self):
        return self.__grade

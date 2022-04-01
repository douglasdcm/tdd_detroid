from enum import Enum
from src.model.course import Course


class Status(Enum):
    pending = "pending"
    open = "open"


class University:
    def __init__(self) -> None:
        self.__status = Status.pending.value
        self.__courses = []
        self.__min_disciplines = 3
        self.__min_courses = 3

    def set_status(self, status):
        self.__status = status

    def get_status(self):
        return self.__status

    def add_course(self, course):
        self.__courses.append(course)

    def create(self):
        if len(self.__courses) >= self.__min_courses:
            for course in self.__courses:
                if len(course.get_disciplines()) < self.__min_disciplines:
                    return False
            self.__status = Status.open.value
            return True
        else:
            return False

    def get_courses(self):
        if self.__status == Status.pending.value:
            return []
        return self.__courses

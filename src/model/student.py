from enum import Enum


class Status(Enum):
    approved = "approved"
    undefined = "undefined"


class Student:
    def __init__(self) -> None:
        self.__score = 0
        self.__disciplines = []

    def update_discipline(self, discipline):
        ids = []
        for discipline_ in self.__disciplines:
            ids.append(discipline_.get_id())
        if discipline.get_id() not in ids:
            self.__disciplines.append(discipline)

    def set_score(self, score):
        self.__score = score
        return True

    def get_status(self):
        return (
            Status.approved.value if self.get_score() >= 7 else Status.undefined.value
        )

    def get_score(self):
        if len(self.__disciplines) > 0:
            grade_sum = 0
            for discipline in self.__disciplines:
                grade_sum += discipline.get_grade()
            self.__score = grade_sum / len(self.__disciplines)
        return self.__score

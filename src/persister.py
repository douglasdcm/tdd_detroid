class Persister:
    def __init__(self):
        self.__students = []
        self.__disciplines = []

    def save_discipline(self, id_, discipline):
        if len(self.__disciplines) <= id_:
            self.__disciplines.append(discipline)
            return
        self.__disciplines[id_] = discipline

    def get_discipline(self, id_):
        if len(self.__disciplines) < id_:
            return None
        discipline = self.__disciplines[id_]
        return discipline

    def save_student(self, id_, student):
        if len(self.__students) <= id_:
            self.__students.append(student)
            return
        self.__students[id_] = student

    def get_student(self, id_):
        if len(self.__students) < id_:
            return None
        student = self.__students[id_]
        return student

from src.model.aluno import Aluno
from src.model.materia import Materia


class StudentManager:
    def __init__(self, student: Aluno):
        self.__student = student

    def update_grade(self, discipline: Materia, grade: float):
        self.__student.update_discipline(discipline, grade)
        self.__student.set_score(grade)

    def __calculate_score(self):
        quantidade = 0
        soma_notas = 0
        disciplines = self.__student.get_disciplines()
        for key in disciplines:
            soma_notas += self.__student.__disciplines[key]
            quantidade += 1
        if soma_notas > 0:
            score = soma_notas / quantidade
        return score

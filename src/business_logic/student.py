from src.utils.exceptions import ErroAluno


class StudentBL:
    def clear_name(self, name):
        name = name.strip()
        if len(name) == 0:
            raise ErroAluno("Invalid student name")
        return name

    def check_grade_boundaries(self, nota):
        if nota > 10:
            raise ErroAluno("Nota não pode ser maior que 10")
        if nota < 0:
            raise ErroAluno("Nota não pode ser menor que 0")

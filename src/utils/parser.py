from src.schemes.for_association import MateriaAlunoBd
from src.schemes.student import AlunoBd


def parse_student(res):
    aluno = AlunoBd()
    aluno.id = res.get("id")
    aluno.coef_rend = res.get("coef_rend")
    aluno.curso_id = res.get("curso_id")
    aluno.nome = res.get("nome")
    return aluno


def parse_discipine_student(res):
    materia_aluno = MateriaAlunoBd()
    materia_aluno.id = res.get("id")
    materia_aluno.aluno_id = res.get("aluno_id")
    materia_aluno.materia_id = res.get("materia_id")
    materia_aluno.aluno_nota = res.get("aluno_nota")
    return materia_aluno

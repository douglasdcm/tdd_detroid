from src.model.aluno import Aluno


class InscricaoAlunoCurso:

    def __init__(self, aluno_id, curso_id):
        self._aluno_id = aluno_id
        self._curso_id = curso_id

    def pega_aluno_id(self):
        return self._aluno_id

    def pega_curso_id(self):
        return self._curso_id

    def atualiza_aluno(self, aluno, curso):
        aluno.inscreve_curso(curso)
        aluno.calcula_situacao()
        return aluno

from src.model.aluno import Aluno
from src.model.curso import Curso


class InscricaoAlunoCurso:
    def __init__(self, aluno, curso):
        """
        Args:
            aluno (Aluno)
            curso (Curso)
        """
        self._aluno = aluno
        self._curso = curso

    def pega_aluno(self) -> Aluno:
        return self._aluno

    def pega_curso(self) -> Curso:
        return self._curso

    def atualiza_aluno(self, aluno):
        self._aluno = aluno

    def atualiza_curso(self, curso):
        self._curso = curso

from src.model.curso import Curso


class Coordenador:
    def __init__(self):
        self._alunos = list()

    def __pega_alunos(self, curso):
        for aluno in curso.pega_lista_alunos():
            alunos = {
                "nome": aluno.pega_nome(),
                "materias": aluno.pega_materias_cursadas(),
                "coeficiente rendimento": aluno.pega_coeficiente_rendimento(),
                "curso": curso.pega_nome(),
            }
            self._alunos.append(alunos)
        return self._alunos

    def listar_detalhe_alunos(self, cursos):
        if isinstance(cursos, list):
            for meu_curso in cursos:
                self.__pega_alunos(meu_curso)
        if isinstance(cursos, Curso):
            self.__pega_alunos(cursos)
        return {"alunos": self._alunos}

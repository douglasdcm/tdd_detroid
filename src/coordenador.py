class Coordenador:
    def __init__(self, curso):
        self._curso = curso
        self._alunos = list()
    def listar_detalhe_alunos(self):
        for aluno in self._curso.pega_lista_alunos(): 
            alunos = {
                "nome": aluno.pega_nome(),
                "materias": aluno.pega_materias_cursadas(),
                "coeficiente rendimento": aluno.pega_coeficiente_rendimento()
            }
            self._alunos.append(alunos)
        return {"alunos": self._alunos}
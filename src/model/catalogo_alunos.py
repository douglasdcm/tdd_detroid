class CatalogoAlunos:

    def __init__(self):
        self._catalogo = list()

    def adiciona_aluno(self, aluno):
        """
        Args:
            aluno (Aluno)
        """
        self._catalogo.append(aluno)

from src.model.i_catalogo import ICatalogo


class CatalogoAlunos(Catalogo):

    def __init__(self, aluno):
        self._catalogo = list()

    def adiciona(self, aluno):
        """
        Args:
            aluno (Aluno)
        """
        self._catalogo.append(aluno)

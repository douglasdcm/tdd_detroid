class AlunoNaoEncontrado(Exception):
    def __init__(self, mensagem="Aluno não encontrado."):
        super().__init__(mensagem)

class CursoNaoEncontrado(Exception):
    def __init__(self, mensagem="Curso não encontrado."):
        super().__init__(mensagem)

class ErroBancoDados(Exception):
    def __init__(self, mensagem="Erro no banco de dados."):
        super().__init__(mensagem)
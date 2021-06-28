class AlunoNaoEncontrado(Exception):
    def __init__(self, mensagem="Aluno não encontrado."):
        super().__init__(mensagem)


class CursoNaoEncontrado(Exception):
    def __init__(self, mensagem="Curso não encontrado."):
        super().__init__(mensagem)


class ErroBancoDados(Exception):
    def __init__(self, mensagem="Erro no banco de dados."):
        super().__init__(mensagem)


class ErroMateriaSemNome(Exception):
    def __init__(self, mensagem="Matéria especificada sem nome."):
        super().__init__(mensagem)


class MaximoCaracteres(Exception,):
    def __init__(self, mensagem="Número de letras excedeu o máximo permitido."):
        super().__init__(mensagem)


class ErroObjetoDaoNaoEncontrado(Exception):
    def __init__(self, mensagem="Objeto não identificado"):
        super().__init__(mensagem)

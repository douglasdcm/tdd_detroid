class AlunoNaoEncontrado(Exception):
    def __init__(self, menssagem="Aluno não encontrado."):
        super().__init__(menssagem)


class CursoNaoEncontrado(Exception):
    def __init__(self, menssagem="Curso não encontrado."):
        super().__init__(menssagem)


class ErroBancoDados(Exception):
    def __init__(self, menssagem="Erro no banco de dados."):
        super().__init__(menssagem)


class ErroMateriaSemNome(Exception):
    def __init__(self, menssagem="Matéria especificada sem nome."):
        super().__init__(menssagem)


class MaximoCaracteres(Exception):
    def __init__(self, menssagem="Número de letras excedeu o máximo permitido."):
        super().__init__(menssagem)


class UnidadeInvalida(Exception):
    def __init__(self, menssagem="Unidade inválida."):
        super().__init__(menssagem)


class CursoCancelado(Exception):
    def __init__(self, menssagem="O curso está cancelado."):
        super().__init__(menssagem)


class CursoUnico(Exception):
    def __init__(self, menssagem="Apenas um curso é permitido."):
        super().__init__(menssagem)


class ComandoInvalido(Exception):
    def __init__(self, menssagem="O comando não foi reconehecido como um comando válido."):
        super().__init__(menssagem)


class ListaParametrosInvalida(Exception):
    def __init__(self, menssagem="Lista de parâmetros inválida."):
        super().__init__(menssagem)


class ErroObjetoDaoNaoEncontrado(Exception):
    def __init__(self, menssagem="Objeto não identificado"):
        super().__init__(menssagem)

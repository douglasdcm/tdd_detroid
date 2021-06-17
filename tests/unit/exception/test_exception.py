from src.model.banco_dados import BancoDados
from pytest import raises


class TestExceptionTraning:

    def test_retorna_excecao_por_try_except(self):
        mensagem = "Exceção por try > except."
        with raises(Exception1, match=mensagem):
            self._retorna_excecao_try_except(mensagem)

    def test_excecao_retornada_sempre(self):
        mensagem = "Excecao sempre."
        with raises(Exception1, match=mensagem):
            self._retorna_excecao_sempre(mensagem)

    def test_excecao_retornada_com_mensagem_constante(self):
        mensagem = "Mensagem padrao constante."
        with raises(Exception2, match=mensagem):
            self._retorna_excecao_com_mensagem_padrao()

    def test_retorna_excecao_por_if(self):
        mensagem = "Excecao por if."
        entrada = True
        with raises(Exception1, match=mensagem):
            self._retorna_excecao_por_if(entrada, mensagem)

    def test_retorna_excecao_funcao_caller(self):
        mensagem = "Exceção por caller."
        with raises(Exception1, match=mensagem):
            self._retorna_excecao_caller(mensagem)

    def _retorna_excecao_caller(self, mensagem):
        try:
            self._retorna_excecao_com_mensagem_padrao()
        except Exception:
            raise Exception1(mensagem)

    def _retorna_excecao_por_if(self, entrada, mensagem):
        if entrada is True:
            raise Exception1(mensagem)

    def _retorna_excecao_com_mensagem_padrao(self):
        raise Exception2()

    def _retorna_excecao_sempre(self, mensagem):
        raise Exception1(mensagem)

    def _retorna_excecao_try_except(self, mensagem):
        try:
            BancoDados(conexao=None).cria_tabela(None, None)
        except Exception:
            raise Exception1(mensagem)


class Exception1(Exception):
    def __init__(self, mensagem="Mensagem padrão."):
        super().__init__(mensagem)


class Exception2(Exception):
    def __init__(self):
        mensagem = "Mensagem padrao constante."
        super().__init__(mensagem)

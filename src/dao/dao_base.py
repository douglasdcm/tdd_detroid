from src.model.i_model import IModel
from src.model.banco_dados import BancoDados
from src.dao.dao_interface import IDao


class DaoBase(IDao):
    def __init__(self, bd: BancoDados, tabela, campos, complemento=""):
        self._bd = bd
        self._tabela = tabela
        self._campos = campos
        self._bd.cria_tabela(self._tabela, self._campos, complemento)

    def deleta(self, id_):
        self._bd.deleta_registro(self._tabela, id_)

    def pega_por_id(self, id_):
        return self._bd.pega_registro_por_id(self._tabela, id_)

    def pega_por_nome(self, nome):
        return self._bd.pega_registro_por_nome(self._tabela, nome)

    def pega_tudo(self):
        return self._bd.pega_todos_registros(self._tabela)

    def pega_por_query(self, query):
        return self._bd.pega_por_query(self._tabela, query)

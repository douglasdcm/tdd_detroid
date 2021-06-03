from os import set_blocking
from src.dao.dao_interface import IDao

class DaoBase(IDao):
    def __init__(self, bd, tabela, campos):
        self._bd = bd
        self._tabela = tabela
        self._campos = campos
        self._bd.cria_tabela(self._tabela, self._campos)

    def pega_por_id(self, id):
        return self._bd.pega_registro_por_id(self._tabela, id)

    def pega_tudo(self):
        return self._bd.pega_todos_registros(self._tabela)

    def pega_por_query(self, query):
        return self._bd.pega_por_query(self._tabela, query)


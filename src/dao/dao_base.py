from src.dao.dao_interface import IDao

class DaoBase(IDao):
    def __init__(self, bd, tabela, campos):
        self._bd = bd
        self._tabela = tabela
        self._campos = campos
        self._bd.cria_tabela(self._tabela, self._campos)

    def pega_tudo(self):
        return self._bd.pega_todos_registros(self._tabela)

import sqlite3


class Tabela:
    def __init__(self, tipo) -> None:
        self.__nome = tipo.__name__.lower()
        self.__colunas = None

    @property
    def colunas(self):
        return self.__colunas

    @colunas.setter
    def colunas(self, valor):
        self.__colunas = valor

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        self.__nome = valor


class BancoDados:
    def __init__(self, nome_banco) -> None:
        self._con = sqlite3.connect(nome_banco)
        self._cursor = self._con.cursor()

    def cria_tabela(self, tabela: Tabela):
        query = f"create table if not exists {tabela.nome} (id INTEGER NOT NULL PRIMARY KEY, '{tabela.colunas}')"
        return self.__execute(query)

    def deleta_tabela(self, tipo):
        query = f"drop table {tipo.__name__.lower()}"
        self.__execute(query)

    def cria(self, tipo, item):
        """
        :item dicionário com os compos e valores do registro
            por exemplo: item = {"nome": "Ana", "idade": 25}
        """
        for k, v in item.items():
            if isinstance(v, str):
                v = f"'{v}'"
            query = f"insert into {tipo.__name__.lower()} ('{k.lower()}') values ({v})"
            self.__execute(query)
        return True

    def lista_maximo(self, tipo):
        tabela_ = tipo.__name__.lower()
        query = "select * from {} where id = ( select max(id) from {} );".format(
            tabela_, tabela_
        )
        return self.__execute(query)

    def lista_tudo(self, tipo):
        query = f"select * from {tipo.__name__.lower()}"
        return self.__execute(query)

    def lista(self, tipo, id_):
        query = f"select * from {tipo.__name__.lower()} where id = {id_}"
        return self.__execute(query)

    def __execute(self, query):
        self._cursor.execute(query)
        self._con.commit()
        return self._cursor.fetchall()

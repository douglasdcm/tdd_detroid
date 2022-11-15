import sqlite3


class Tabela:
    def __init__(self, tipo) -> None:
        self._nome = tipo
        self._colunas = None
        self._chave_estrangeira = None

    @property
    def colunas(self):
        return self._colunas

    @colunas.setter
    def colunas(self, valor):
        self._colunas = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = valor

    @property
    def chave_estrangeira(self):
        return self._chave_estrangeira

    @chave_estrangeira.setter
    def chave_estrangeira(self, valor):
        """
        : valor coluna, tipo_alvo, coluna_alvo
        """
        self._chave_estrangeira = valor


class BancoDados:
    def __init__(self, nome_banco) -> None:
        self._con = sqlite3.connect(nome_banco)
        self._cursor = self._con.cursor()
        # habilita as chaves estrangeiras
        self.__execute("PRAGMA foreign_keys = ON")

    def cria_tabela(self, tabela: Tabela):
        colunas_formatadas = ""
        for coluna in tabela.colunas:
            colunas_formatadas += f"'{coluna}',"
        colunas_formatadas = colunas_formatadas[:-1]
        complemento = ""
        if tabela.chave_estrangeira:
            complemento = f",FOREIGN KEY ({tabela.chave_estrangeira[0]}) REFERENCES {tabela.chave_estrangeira[1]} ({tabela.chave_estrangeira[2]})"

        query = f"create table if not exists {tabela.nome} (id INTEGER NOT NULL PRIMARY KEY, {colunas_formatadas} {complemento})"
        return self.__execute(query)

    def deleta_tabela(self, tipo):
        query = f"drop table {tipo}"
        self.__execute(query)

    def cria(self, tipo, item):
        """
        :item dicionário com os compos e valores do registro
            por exemplo: item = {"nome": "Ana", "idade": 25}
        """
        k_formatada = ""
        v_formatado = ""
        for k, v in item.items():
            if isinstance(v, str):
                v = f"'{v}'"
            k_formatada += f"'{k}',"
            v_formatado += f"{v},"
        query = f"insert into {tipo} ({k_formatada[:-1]}) values ({v_formatado[:-1]})"
        self.__execute(query)
        return True

    def lista_maximo(self, tipo):
        query = f"select * from {tipo} where id = ( select max(id) from {tipo} );"
        return self.__execute(query)

    def lista_tudo(self, tipo):
        query = f"select * from {tipo}"
        return self.__execute(query)

    def lista(self, tipo, id_):
        query = f"select * from {tipo} where id = {id_}"
        return self.__execute(query)

    def roda_query(self, query):
        return self.__execute(query)

    def __execute(self, query):
        try:
            self._cursor.execute(query)
            self._con.commit()
            return self._cursor.fetchall()
        except Exception as e:
            raise ErroBancoDados(e)


class ErroBancoDados(Exception):
    pass

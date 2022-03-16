from src.exceptions.exceptions import ErroBancoDados


class BancoDados:

    _conexao = None

    def __init__(self, conexao=None):
        if type(self)._conexao is None:
            if conexao is not None:
                type(self)._conexao = conexao
            else:
                raise ErroBancoDados("Uma conexão precisa ser informada.")

    def _liga_foreing_key_support(self):
        try:
            items = self._cria_conexao()
            cur = items[1]
            cur.execute("PRAGMA foreign_keys = OFF")
        except Exception:
            raise ErroBancoDados("Não foi possível ligar o foreing_key_support.")

    def deleta_tabela(self, tabela):
        try:
            items = self._cria_conexao()
            cur = items[1]
            cur.execute(f"drop table if exists {tabela}")
        except Exception:
            raise ErroBancoDados("Não foi possível deletar a tabela.")

    def fecha_conexao_existente(self):
        try:
            con = type(self)._conexao
            con.close()
            type(self)._conexao = None
            return True
        except Exception:
            return False

    def _cria_conexao(self):
        try:
            con = type(self)._conexao
            cur = con.cursor()
            return [con, cur]
        except Exception:
            raise ErroBancoDados("Não foi possível criar a conexão de banco.")

    def cria_tabela(self, tabela, campos, complemento=""):
        if complemento:
            complemento = "," + complemento
        query = f"create table if not exists {tabela} (id INTEGER NOT NULL PRIMARY KEY, {campos} {complemento})"
        mensagem_erro = "Não foi possível criar a tabela."
        self._run(query, mensagem_erro)

    def create_table(self, table: dict):
        query = (
            "CREATE TABLE IF NOT EXISTS {} (id INTEGER NOT NULL PRIMARY KEY, ".format(
                table["name"].upper()
            )
        )
        names = ""
        for column in table["columns"]:
            names += column["name"].upper() + " "
            names += column["type"].upper() + " "
            names += column["constraints"].upper() + ", "
        query += names[:-2] + ");"
        self._run(query)
        return query

    def atualiza_registro(self, tabela, sets, id_):
        query = f"""UPDATE {tabela}
                SET {sets}
                WHERE id = {id_};"""
        mensagem_erro = "Não foi possível atualizar o registro."
        self._run(query, mensagem_erro)

    def save(self, table: str, records: list):
        """Retorn a True if the record is saved"""
        for record in records:
            query = "insert into {} ".format(table)
            columns = values = ""
            for k, v in record.items():
                columns += "{}, ".format(k)
                if isinstance(v, str):
                    v = '"{}"'.format(v)
                values += "{}, ".format(v)
            query += "({}) values ({})".format(columns[:-2], values[:-2])
            result = self._run(query)
        return query, result

    def salva_registro(self, tabela, campos, valores):
        """Retorna a tupla com o maior id da tabela"""
        query = f"insert into {tabela} ({campos}) values ({valores})"
        mensagem_erro = "Não foi possiível salvar o registro."
        self._run(query, mensagem_erro)
        return self.pega_maior_id(tabela)

    def get_by_id(self, columns: list, table, id_):
        cols = ""
        for column in columns:
            cols += column + ", "
        query = "SELECT {} FROM {} WHERE ID = {}".format(
            cols[:-2].upper(), table.upper(), id_
        )
        result = self._run(query)
        return query, result

    def pega_maior_id(self, tabela):
        query = "SELECT * FROM {} WHERE id = ( SELECT MAX(id) FROM {} );".format(
            tabela, tabela
        )
        mensagem_erro = "Não foi possível pegar o ID máximo."
        return self._run(query, mensagem_erro)

    def get_biggest_id(self, table):
        return self.pega_maior_id(table)

    def deleta_registro(self, tabela, id_):
        query = f"delete from {tabela} where id = {id_}"
        mensagem_erro = "Não foi possível excluir o registro especificado."
        self._run(query, mensagem_erro)

    def pega_todos_registros(self, tabela):
        query = f"select * from {tabela}"
        mensagem_erro = "Não foi possível pegar os registros."
        return self._run(query, mensagem_erro)

    def pega_registro_por_id(self, tabela, id_):
        """Retorna a tupla da tabela identificada pelo id"""
        query = f"select * from {tabela} where id = {id_}"
        mensagem_erro = "Não foi possível pegar o registro especificado."
        result = self._run(query, mensagem_erro)
        if result == []:
            raise ErroBancoDados(
                f"Registro especificado de identificador {id_} não foi encontrado."
            )
        else:
            return result

    def pega_registro_por_nome(self, tabela, nome):
        query = f"select * from {tabela} where nome = '{nome}'"
        mensagem_erro = "Não foi possível pegar o registro especificado."
        result = self._run(query, mensagem_erro)
        if result == []:
            raise ErroBancoDados(f"Registro especificado '{nome}' não foi encontrado.")
        else:
            return result

    def pega_por_query(self, query):
        mensagem_erro = "Não foi possível executar a query especificada."
        return self._run(query, mensagem_erro)

    def _run(self, query, mensagem_erro=""):
        """
        Args:
            query (str): consulta sql a ser executada
            mensagem_erro (str): menssagem retornada em caso de erro na execução

        Returns:
            (tuple): tupla com os registros do banco de dados
        """
        try:
            items = self._cria_conexao()
            con = items[0]
            cur = items[1]
            cur.execute(query)
            con.commit()
            return cur.fetchall()
        except Exception as e:
            raise ErroBancoDados(
                "\nIt was not possible to run the command '{}'\n Trace: {}".format(
                    query, e
                )
            )

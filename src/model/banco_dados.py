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
            cur.execute(f"PRAGMA foreign_keys = OFF")
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

    def salva_registro(self, tabela, campos, valores):
        query = f"insert into {tabela} ({campos}) values ({valores})"
        mensagem_erro = "Não foi possiível salvar o registro."
        self._run(query, mensagem_erro)

    def deleta_registro(self, tabela, id):
        query = f"delete from {tabela} where id = {id}"
        mensagem_erro = "Não foi possível excluir o registro especificado."
        self._run(query, mensagem_erro)

    def pega_todos_registros(self, tabela):
        query = f"select * from {tabela}"
        mensagem_erro = "Não foi possível pegar os registros."
        return self._run(query, mensagem_erro)

    def pega_registro_por_id(self, tabela, id):
        query = f"select * from {tabela} where id = {id}"
        mensagem_erro = "Não foi possível pegar o registro especificado."
        result = self._run(query, mensagem_erro)
        if result == []:
            raise ErroBancoDados(f"Registro especificado não foi encontrado.")
        else:
            return result

    def pega_por_query(self, tabela, query):
        mensagem_erro = "Não foi possível executar a query especificada."
        return self._run(query, mensagem_erro)

    def _run(self, query, mensagem_erro):
        try:
            items = self._cria_conexao()
            con = items[0]
            cur = items[1]
            cur.execute(query)
            con.commit()
            return cur.fetchall()
        except Exception:
            raise ErroBancoDados(f"{mensagem_erro}\nquery: {query}")

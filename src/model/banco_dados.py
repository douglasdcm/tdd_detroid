class BancoDados:

    _conexao = None

    def __init__(self, conexao=None):
        if type(self)._conexao is None:
            if conexao is not None:            
                type(self)._conexao = conexao
            else:
                raise Exception("Uma conexão precisa ser informada.")            

    def deleta_tabela(self, tabela):
        try:
            items = self._cria_conexao()
            cur = items[1] 
            cur.execute(f"drop table if exists {tabela}")
        except Exception:
            raise Exception("Não foi possível deletar a tabela.")

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
            raise Exception("Não foi possível criar a conexão de banco.")

    def cria_tabela(self, tabela, campos):
        try:
            items = self._cria_conexao()
            con = items[0]
            cur = items[1] 
            query = f"create table if not exists {tabela} (id INTEGER NOT NULL PRIMARY KEY, {campos})"
            cur.execute(query)
            con.commit()
        except Exception:
            raise Exception("Não foi possível criar a tabela.")

    def salva_registro(self, tabela, campos, valores):
        try:
            items = self._cria_conexao()
            con = items[0]
            cur = items[1]    
            cur.execute(f"insert into {tabela} ({campos}) values ({valores})")
            con.commit()
        except Exception:
            raise Exception("Não foi possiível salvar o registro.")

    def pega_todos_registros(self, tabela):
        try:
            items = self._cria_conexao()
            cur = items[1]
            cur.execute(f"select * from {tabela}")
            return cur.fetchall()
        except Exception:
            raise Exception("Não foi possível pegar os registros.")



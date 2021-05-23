class BancoDados:

    _conexao = None

    def __init__(self, conexao=None):
        if type(self)._conexao is None:
            if conexao is not None:            
                type(self)._conexao = conexao
            else:
                raise Exception("Uma conexão precisa ser informada.")            

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
            cur.execute(f"create table if not exists {tabela} ({campos})")
            con.commit()
        except Exception:
            raise Exception("Não foi possível criar a tabela.")

    def salva_registro(self, tabela, valores):
        try:
            items = self._cria_conexao()
            con = items[0]
            cur = items[1]   
            print(f"insert into {tabela} values ({valores})")     
            cur.execute(f"insert into {tabela} values ({valores})")
            con.commit()
        except Exception:
            raise Exception("Não foi possiível salvar o registro.")

    def pega_todos_registros(self, tabela):
        try:
            items = self._cria_conexao()
            cur = items[1]
            cur.execute(f"select * from {tabela}")
            return cur.fetchmany()
        except Exception:
            raise Exception("Não foi possível pegar os registros.")



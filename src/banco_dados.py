import sqlite3

class BancoDados:

    def cria_conexao(self):
        try:
            con = sqlite3.connect("sample.db")
            cur = con.cursor()
            return [con, cur]
        except Exception:
            raise Exception("Não foi possível criar a conexão de banco.")

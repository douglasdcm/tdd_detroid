import sqlite3

class TestDatabase:

    def test_criacao_de_tabela_de_alunos(self):
        expected = 1
        con = sqlite3.connect(":memory:")
        cur = con.cursor()
        cur.execute("create table alunos (name, materia)")
        cur.execute("insert into alunos values ('aluno_1', 1)")
        cur.execute("select * from alunos")
        actual = cur.lastrowid
        assert actual == expected

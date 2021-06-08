from tests.helper import executa_comando
from tests.massa_dados import aluno_nome_1, curso_nome_1
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.controller.controller import Controller
from src.tabelas import inscricao_aluno_curso, alunos, cursos
from pytest import fixture, raises

class TestCliInscreveAlunoCurso:   

    @fixture(autouse=True, scope="function")
    def setup(self, cria_banco_real):
        self.aluno_id = self.curso_id  = "1"
        bd = cria_banco_real
        bd.deleta_tabela(inscricao_aluno_curso)
        bd.deleta_tabela(cursos)
        bd.deleta_tabela(alunos)

    def test_retorna_excecao_quando_curso_id_nao_existe(self, cria_aluno_banco_real):
        expected = "Curso não encontrado."
        parametros = ["inscreve-aluno-curso", "--aluno-id", self.aluno_id, "--curso-id",
            self.curso_id]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_retorna_excecao_quando_aluno_id_nao_existe(self, cria_curso_banco_real):
        expected = "Aluno não encontrado."
        parametros = ["inscreve-aluno-curso", "--aluno-id", self.aluno_id, "--curso-id",
            self.curso_id]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_aluno_pode_ser_inscrito_curso(self, cria_massa_dados):
        expected = f"Aluno identificado por {self.aluno_id} inscrito no curso identificado por {self.curso_id}."
        parametros = ["inscreve-aluno-curso", "--aluno-id", self.aluno_id, "--curso-id",
                self.curso_id]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_aluno_inscrito_curso_salvo_banco_dados(self, cria_banco_real, cria_massa_dados):
        expected = [tuple((1, self.aluno_id, self.curso_id))]
        parametros = ["inscreve-aluno-curso", "--aluno-id", self.aluno_id, "--curso-id",
                self.curso_id]
        executa_comando(parametros)
        inscricao = InscricaoAlunoCurso(self.aluno_id, self.curso_id)
        actual = Controller(inscricao, cria_banco_real).pega_registros()
        assert actual == expected
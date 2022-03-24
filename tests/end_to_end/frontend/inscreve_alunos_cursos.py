from _pytest.python import Instance
from tests.helper import executa_comando
from pytest import fixture
from src.tabelas import alunos, cursos, inscricao_aluno_curso


class TestIncricaoAlunosCursos:
    def test_inscreve_um_aluno_em_um_curso(self):
        expected = "Aluno identificado por 1 inscrito no curso identificado por 1."
        parametros_aluno = self._cria_aluno("Douglas")
        parametros_curso = self._cria_curso("Adm")
        parametros_inscricao = self._inscreve_curso(aluno_id="1", curso_id="1")
        executa_comando(parametros_aluno)
        executa_comando(parametros_curso)
        actual = executa_comando(parametros_inscricao)
        assert expected in actual

    def test_inscreve_dois_alunos_em_um_curso(self):
        expected = "Aluno identificado por 2 inscrito no curso identificado por 1."
        parametros_aluno_1 = self._cria_aluno("Douglas")
        parametros_aluno_2 = self._cria_aluno("Cláudia")
        parametros_curso = self._cria_curso("Adm")
        parametros_inscricao_1 = self._inscreve_curso(aluno_id="1", curso_id="1")
        parametros_inscricao_2 = self._inscreve_curso(aluno_id="2", curso_id="1")
        executa_comando(parametros_aluno_1)
        executa_comando(parametros_aluno_2)
        executa_comando(parametros_curso)
        executa_comando(parametros_inscricao_1)
        actual = executa_comando(parametros_inscricao_2)
        assert expected in actual

    def test_inscreve_um_aluno_em_dois_cursos(self):
        aluno_id = "1"
        curso_id_1 = "1"
        curso_id_2 = "2"
        expected = "Aluno identificado por 1 inscrito no curso identificado por 2."
        parametros_aluno = self._cria_aluno("Douglas")
        parametros_curso_1 = self._cria_curso("Adm")
        parametros_curso_2 = self._cria_curso("Pat")
        parametros_inscricao_1 = self._inscreve_curso(aluno_id, curso_id_1)
        parametros_inscricao_2 = self._inscreve_curso(aluno_id, curso_id_2)
        executa_comando(parametros_aluno)
        executa_comando(parametros_curso_1)
        executa_comando(parametros_curso_2)
        executa_comando(parametros_inscricao_1)
        actual = executa_comando(parametros_inscricao_2)
        assert expected in actual

    def _cria_aluno(self, nome):
        return ["cria-aluno", "--nome", nome]

    def _cria_curso(self, nome):
        return ["cria-curso", "--nome", nome, "--materias", "m1", "m2", "m3"]

    def _inscreve_curso(self, aluno_id, curso_id):
        return ["inscreve-aluno-curso", "--aluno-id", aluno_id, "--curso-id", curso_id]

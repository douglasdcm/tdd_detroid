from src.model.curso import Curso
from src.model.aluno import Aluno
from src.model.materia import Materia
from tests.helper import executa_comando
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.controller.controller import Controller
from src.tabelas import inscricao_aluno_curso, alunos, cursos
from pytest import fixture
from tests.massa_dados import (
    aluno_nome_1,
    curso_nome_1,
    materia_nome_1,
    materia_nome_2,
    materia_nome_3,
)


class TestCliInscreveAlunoCurso:
    @fixture(autouse=True, scope="function")
    def setup(self, cria_banco_real):
        self.aluno_id = self.curso_id = "1"
        bd = cria_banco_real
        bd.deleta_tabela(inscricao_aluno_curso)
        bd.deleta_tabela(cursos)
        bd.deleta_tabela(alunos)

    def test_situaca_aluno_muda_para__em_curso__apos_inscricao(self, cria_banco_real):
        aluno = Aluno(aluno_nome_1)
        curso = Curso(curso_nome_1)
        materia_1 = Materia(materia_nome_1)
        materia_2 = Materia(materia_nome_2)
        materia_3 = Materia(materia_nome_3)
        curso.atualiza_materias(materia_1)
        curso.atualiza_materias(materia_2)
        curso.atualiza_materias(materia_3)
        Controller(aluno, cria_banco_real).salva()
        Controller(curso, cria_banco_real).salva()
        expected = "em curso"
        parametros = [
            "inscreve-aluno-curso",
            "--aluno-id",
            self.aluno_id,
            "--curso-id",
            self.curso_id,
        ]
        executa_comando(parametros)
        inscricao = InscricaoAlunoCurso(
            aluno.define_id(self.aluno_id), curso.define_id(self.curso_id)
        )
        Controller(inscricao, cria_banco_real).salva()
        aluno = Controller(aluno, cria_banco_real).pega_registro_por_id(self.aluno_id)
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_retorna_excecao_quando_curso_id_nao_existe(self, cria_banco_real):
        expected = "Curso não encontrado."
        Controller(Aluno(None), cria_banco_real).salva()
        parametros = [
            "inscreve-aluno-curso",
            "--aluno-id",
            self.aluno_id,
            "--curso-id",
            self.curso_id,
        ]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_retorna_excecao_quando_aluno_id_nao_existe(self):
        expected = "Aluno não encontrado."
        parametros = [
            "inscreve-aluno-curso",
            "--aluno-id",
            self.aluno_id,
            "--curso-id",
            self.curso_id,
        ]
        actual = executa_comando(parametros)
        assert expected in actual

    def test_aluno_pode_ser_inscrito_curso(self, cria_curso_banco_real):
        expected = (
            f"Aluno identificado por {self.aluno_id} inscrito no curso"
            f" identificado por {self.curso_id}."
        )
        aluno, curso = cria_curso_banco_real
        parametros = [
            "inscreve-aluno-curso",
            "--aluno-id",
            str(aluno.pega_id()),
            "--curso-id",
            str(curso.pega_id()),
        ]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_aluno_inscrito_curso_salvo_banco_dados(self, cria_banco_real):
        aluno = Aluno(aluno_nome_1)
        curso = Curso(curso_nome_1)
        Controller(aluno, cria_banco_real).salva()
        Controller(curso, cria_banco_real).salva()
        expected = [tuple((1, self.aluno_id, self.curso_id))]
        parametros = [
            "inscreve-aluno-curso",
            "--aluno-id",
            self.aluno_id,
            "--curso-id",
            self.curso_id,
        ]
        executa_comando(parametros)
        inscricao = InscricaoAlunoCurso(
            aluno.define_id(self.aluno_id), curso.define_id(self.curso_id)
        )
        actual = Controller(inscricao, cria_banco_real).pega_registros()
        assert actual == expected

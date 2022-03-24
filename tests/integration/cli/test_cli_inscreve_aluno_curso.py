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
    def test_situaca_aluno_muda_para__em_curso__apos_inscricao(
        self, setup_database_in_real_db
    ):
        aluno = Aluno(aluno_nome_1)
        curso = Curso(curso_nome_1)
        materia_1 = Materia(materia_nome_1)
        materia_2 = Materia(materia_nome_2)
        materia_3 = Materia(materia_nome_3)
        curso.atualiza_materias(materia_1)
        curso.atualiza_materias(materia_2)
        curso.atualiza_materias(materia_3)
        Controller(aluno, setup_database_in_real_db).salva()
        Controller(curso, setup_database_in_real_db).salva()
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
        Controller(inscricao, setup_database_in_real_db).salva()
        aluno = Controller(aluno, setup_database_in_real_db).pega_registro_por_id(
            self.aluno_id
        )
        actual = aluno.pega_situacao()
        assert actual == expected

    def test_retorna_excecao_quando_curso_id_nao_existe(
        self, setup_database_in_real_db
    ):
        expected = "Curso não encontrado."
        Controller(Aluno(None), setup_database_in_real_db).salva()
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

    def test_aluno_pode_ser_inscrito_curso(self, setup_database_in_real_db):
        aluno_id = curso_id = "1"
        expected = (
            f"Aluno identificado por {aluno_id} inscrito no curso"
            f" identificado por {curso_id}."
        )
        parametros = [
            "inscreve-aluno-curso",
            "--aluno-id",
            aluno_id,
            "--curso-id",
            curso_id,
        ]
        actual = executa_comando(parametros)
        assert actual == expected

    def test_aluno_inscrito_curso_salvo_banco_dados(self, setup_database_in_real_db):
        aluno = Aluno(aluno_nome_1)
        curso = Curso(curso_nome_1)
        Controller(aluno, setup_database_in_real_db).salva()
        Controller(curso, setup_database_in_real_db).salva()
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
        actual = Controller(inscricao, setup_database_in_real_db).pega_registros()
        assert actual == expected

import sqlite3
from src.model.coordenador import Coordenador
from src.model.catalogo_curso import CatalogoCurso
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.model.coordenador_curso import CoordenadorCurso
from src.model.materia import Materia
from src.model.banco_dados import BancoDados
from tests.massa_dados import materia_nome_1, materia_nome_2, materia_nome_3
import pytest


class TestCoordenador:
    coordenador = None

    def setup_method(self, method):
        self.catalogo = CatalogoCurso()
        self.catalogo.limpa_catalogo()
        self.curso = Curso("direito")
        self.curso.atualiza_materias(Materia("civil"))
        self.curso.atualiza_materias(Materia("penal"))
        self.curso.atualiza_materias(Materia("filosofia"))
        self.coordenador = CoordenadorCurso(self.curso)

    def tear_down(self, method):
        self.catalogo.limpa_catalogo()
        self.curso = None
        self.coordenador = None

    def test_coordenador_nao_pode_coordenar_curso_cancelado(self, cria_curso_cancelado):
        curso = cria_curso_cancelado
        with pytest.raises(Exception, match="O coordenador não pode se associar a um curso cancelado"):
            CoordenadorCurso(curso)

    def test_coordenador_pode_listar_info_todos_alunos_dos_cursos(self, cria_curso_com_materias):
        nome_1 = "diogo"
        nome_2 = "miguel"
        curso_1 = cria_curso_com_materias
        curso_1_nome = curso_1.pega_nome()
        curso_2 = self.curso
        curso_2_nome = curso_2.pega_nome()
        materias_1 = {materia_nome_1: 1.0}
        materias_2 = {"civil": 8.0, "penal": 8.0}
        cr_1 = 1.0
        cr_2 = 8.0
        coordenador = CoordenadorCurso(curso_1)
        coordenador.adiciona_cursos(curso_2)
        expected = {"alunos": [
            {
                "nome": nome_1,
                "materias": materias_1,
                "coeficiente rendimento": cr_1,
                "curso": curso_1_nome
            },
            {
                "nome": nome_2,
                "materias": materias_2,
                "coeficiente rendimento": cr_2,
                "curso": curso_2_nome
            },
            ]
        }
        self._cria_aluno_no_curso(nome_1, curso_1, materias_1)
        self._cria_aluno_no_curso(nome_2, curso_2, materias_2)
        actual = coordenador.listar_detalhe_alunos()
        assert actual == expected

    def test_coordenador_pode_coordenar_mais_de_um_curso(self, cria_curso_com_materias):
        curso_1 = cria_curso_com_materias
        curso_2 = cria_curso_com_materias
        curso_3 = cria_curso_com_materias
        expected = curso_3
        cursos = [curso_2, curso_3]
        cursos.append(curso_1)
        coordenador = CoordenadorCurso(curso_1)
        coordenador.adiciona_cursos(cursos)
        actual = coordenador.pega_lista_cursos()
        assert expected in actual

    def test_coordenador_curso_2_nao_pode_listar_alunos_curso_1(self):
        expected = {"alunos": []}
        aluno = Aluno("maria")
        curso = Curso("fisica")
        curso.atualiza_materias(Materia("optica"))
        curso.atualiza_materias(Materia("mecanica"))
        curso.atualiza_materias(Materia("eletrica"))
        coordenador_2 = CoordenadorCurso(curso)
        aluno.inscreve_curso(self.curso)
        actual = coordenador_2.listar_detalhe_alunos()
        assert actual == expected

    def test_coordenador_curso_pode_listar_alunos_do_curso_com_dois_aluno(self):
        nome_1 = "diogo"
        nome_2 = "miguel"
        materias_1 = {"civil": 1}
        materias_2 = {"penal": 8, "civil": 8}
        cr_1 = 1
        cr_2 = 8
        expected = {"alunos": [
            {
                "nome": nome_1,
                "materias": materias_1,
                "coeficiente rendimento": cr_1,
                "curso": self.curso.pega_nome()
            },
            {
                "nome": nome_2,
                "materias": materias_2,
                "coeficiente rendimento": cr_2,
                "curso": self.curso.pega_nome()
            },
            ]
        }
        self._cria_aluno_no_curso(nome_1, self.curso, materias_1)
        self._cria_aluno_no_curso(nome_2, self.curso, materias_2)
        actual = self.coordenador.listar_detalhe_alunos()
        assert actual == expected

    def test_coordenador_curso_pode_listar_alunos_do_curso_com_um_aluno(self):
        nome = "marcos"
        materias = {"civil": 5}
        cr = 5
        expected = {"alunos": [{"nome": nome, "materias": materias,
        "coeficiente rendimento": cr, "curso": self.curso.pega_nome()}]}
        self._cria_aluno_no_curso(nome, self.curso, materias)
        actual = self.coordenador.listar_detalhe_alunos()
        assert actual == expected

    def test_coordenador_curso_pode_listar_alunos_curso_quando_zero_alunos(self):
        expected = {"alunos": []}
        actual = self.coordenador.listar_detalhe_alunos()
        assert actual == expected

    def _cria_aluno_no_curso(self, nome_aluno, curso, materias):
        aluno = Aluno(nome_aluno)
        aluno.inscreve_curso(curso)
        aluno.atualiza_materias_cursadas(materias)

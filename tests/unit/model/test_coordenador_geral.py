from src.controller.controller import Controller
from time import process_time_ns, sleep
import sqlite3

from pytest import fixture
from src.model.catalogo_curso import CatalogoCurso
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.model.coordenador_geral import CoordenadorGeral
from src.model.materia import Materia
from src.model.banco_dados import BancoDados

class TestCoordenadorGeral:

    def setup_method(self, cria_banco):
        self.catalogo = CatalogoCurso()
        self.catalogo.limpa_catalogo()
        self.curso_1 = Curso("direito")
        self.curso_1.atualiza_materias(Materia("civil"))
        self.curso_1.atualiza_materias(Materia("penal"))
        self.curso_1.atualiza_materias(Materia("filosofia"))
        self.curso_2 = Curso("agricola")
        self.curso_2.atualiza_materias(Materia("solos"))
        self.curso_2.atualiza_materias(Materia("plantas"))
        self.curso_2.atualiza_materias(Materia("animais"))
        self.curso_3 = Curso("engenharia")
        self.curso_3.atualiza_materias(Materia("estrutura"))
        self.curso_3.atualiza_materias(Materia("mecanica"))
        self.curso_3.atualiza_materias(Materia("concreto"))

    def teardown_method(self, method):
        self.catalogo.limpa_catalogo()
        self.curso_1 = None
        self.curso_2 = None
        self.curso_3 = None

    def test_popula_banco(self, cria_banco, cria_massa_dados_em_memoria):
        actual = Controller(Aluno(None), cria_banco).pega_registro_por_id(1)
        actual_2 = Controller(Curso(None), cria_banco).pega_registro_por_id(1)
        assert actual is None

    def test_coordenador_geral_pega_detalhes_alunos_pelo_banco(self):
        expected = {"alunos": [{"nome": "joão", "coeficiente rendimento": 6, "materias": {"m1": 6}}]}
        coordenador = CoordenadorGeral()
        actual = coordenador.listar_detalhe_alunos_por_banco()
        assert actual == expected

    def test_coordenador_geral_lista_detalhes_novo_curso(self):
        nome = "mario"
        aluno = Aluno(nome)
        materias = {"virus": 6}
        expected = {"alunos": [{"nome": nome, "coeficiente rendimento": 6, "materias": materias}]}
        coordenador = CoordenadorGeral()
        curso_novo = Curso("patologia")
        curso_novo.atualiza_materias(Materia("bacterias"))
        curso_novo.atualiza_materias(Materia("virus"))
        curso_novo.atualiza_materias(Materia("vermes"))
        aluno.inscreve_curso(curso_novo)
        aluno.atualiza_materias_cursadas(materias)
        actual = coordenador.listar_detalhe_alunos()
        assert actual == expected

    def test_coordenador_geral_lista_detalhes_dois_cursos_dois_alunos_com_notas(self):
        nome_1 = "joao"
        nome_2 = "maria"
        materias_1 = {"penal": 3}
        materias_2 = {"plantas": 3, "solos": 3}
        cr = 3
        expected = {"alunos": [
            {"nome": nome_1, "coeficiente rendimento": cr, "materias": materias_1},
            {"nome": nome_2, "coeficiente rendimento": cr, "materias": materias_2}
        ]}
        aluno_1 = Aluno(nome_1)
        aluno_2 = Aluno(nome_2)
        aluno_1.inscreve_curso(self.curso_1)
        aluno_2.inscreve_curso(self.curso_2)
        aluno_1.atualiza_materias_cursadas(materias_1)
        aluno_2.atualiza_materias_cursadas(materias_2)
        coordenador = CoordenadorGeral()
        actual = coordenador.listar_detalhe_alunos()
        assert actual == expected

    def test_coordenador_geral_lista_detalhes_quando_dois_cursos_com_alunos(self):
        nome_1 = "joao"
        nome_2 = "maria"
        expected = {"alunos": [
            {"nome": nome_1, "coeficiente rendimento": 0, "materias": {}},
            {"nome": nome_2, "coeficiente rendimento": 0, "materias": {}}
        ]}
        aluno_1 = Aluno(nome_1)
        aluno_2 = Aluno(nome_2)
        aluno_1.inscreve_curso(self.curso_1)
        aluno_2.inscreve_curso(self.curso_2)
        coordenador = CoordenadorGeral()
        actual = coordenador.listar_detalhe_alunos()
        assert actual == expected

    def test_coordenador_geral_lista_detalhes_quando_dois_cursos(self):
        expected = {"alunos": []}
        coordenador = CoordenadorGeral()
        actual = coordenador.listar_detalhe_alunos()
        assert actual == expected


    def test_coordenador_geral_lista_detalhes_quando_dois_alunos(self):
        nome_1 = "joao"
        nome_2 = "maria"
        expected = {"alunos": [
            {"nome": nome_1, "coeficiente rendimento": 0, "materias": {}},
            {"nome": nome_2, "coeficiente rendimento": 0, "materias": {}}
        ]}
        aluno_1 = Aluno(nome_1)
        aluno_2 = Aluno(nome_2)
        aluno_1.inscreve_curso(self.curso_1)
        aluno_2.inscreve_curso(self.curso_1)
        coordenador = CoordenadorGeral()
        actual = coordenador.listar_detalhe_alunos()
        assert actual == expected

    def test_coordenador_geral_lista_detalhes_alunos_quando_um_aluno(self):
        nome = "maria"
        materias = {"civil": 6}
        cr = 6
        expected = {"alunos":[
                    {
                        "nome": nome,
                        "materias": materias,
                        "coeficiente rendimento": cr
                    }
                ]
            }
        aluno = Aluno("maria")
        aluno.inscreve_curso(self.curso_1)
        aluno.atualiza_materias_cursadas(materias)
        coordenador = CoordenadorGeral()
        actual = coordenador.listar_detalhe_alunos()
        assert actual == expected

    def test_cooredenador_geral_lista_detalhes_quando_zero_alunos(self):
        expected = {"alunos": []}
        coordenador = CoordenadorGeral()
        actual = coordenador.listar_detalhe_alunos()
        assert actual == expected

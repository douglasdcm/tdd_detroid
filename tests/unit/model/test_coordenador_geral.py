from src.model.catalogo_curso import CatalogoCurso
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.model.coordenador_geral import CoordenadorGeral
from src.model.materia import Materia


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

    def test_define_id_retorna_coordenador_com_id_atualizado(self):
        expected = 1
        coordenador = CoordenadorGeral().define_id(expected)
        actual = coordenador.pega_id()
        assert actual == expected

    def test_coordenador_geral_lista_detalhes_novo_curso(self):
        nome = "mario"
        curso = "patologia"
        aluno = Aluno(nome)
        materias = {"virus": 6}
        expected = {"alunos": [{"nome": nome, "coeficiente rendimento": 6,
                    "materias": materias, "curso": curso}]}
        coordenador = CoordenadorGeral()
        curso_novo = Curso(curso)
        curso_novo.atualiza_materias(Materia("bacterias"))
        curso_novo.atualiza_materias(Materia("virus"))
        curso_novo.atualiza_materias(Materia("vermes"))
        aluno.inscreve_curso(curso_novo)
        aluno.atualiza_materias_cursadas(materias)
        actual = coordenador.listar_detalhe_alunos()
        assert actual == expected

    def test_coordenador_geral_lista_detalhe_2_cursos_2_alunos_com_notas(self):
        nome_1 = "joao"
        nome_2 = "maria"
        materias_1 = {"penal": 3}
        materias_2 = {"plantas": 3, "solos": 3}
        cr = 3
        expected = {"alunos": [
            {"nome": nome_1, "coeficiente rendimento": cr,
             "materias": materias_1, "curso": self.curso_1.pega_nome()},
            {"nome": nome_2, "coeficiente rendimento": cr,
             "materias": materias_2, "curso": self.curso_2.pega_nome()}
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

    def test_coordenador_geral_lista_detalhes_quando_2_cursos_com_alunos(self):
        nome_1 = "joao"
        nome_2 = "maria"
        expected = {"alunos": [
            {"nome": nome_1, "coeficiente rendimento": 0, "materias": {}, "curso": self.curso_1.pega_nome()},
            {"nome": nome_2, "coeficiente rendimento": 0, "materias": {}, "curso": self.curso_2.pega_nome()}
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
            {"nome": nome_1, "coeficiente rendimento": 0, "materias": {}, "curso": self.curso_1.pega_nome()},
            {"nome": nome_2, "coeficiente rendimento": 0, "materias": {}, "curso": self.curso_1.pega_nome()}
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
        expected = {"alunos": [
                            {
                                "nome": nome,
                                "materias": materias,
                                "coeficiente rendimento": cr,
                                "curso": self.curso_1.pega_nome()
                            }
                        ]
                    }
        aluno = Aluno("maria")
        aluno.inscreve_curso(self.curso_1)
        aluno.atualiza_materias_cursadas(materias)
        coordenador = CoordenadorGeral()
        actual = coordenador.listar_detalhe_alunos()
        assert actual == expected

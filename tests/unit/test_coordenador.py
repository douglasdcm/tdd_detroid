import sqlite3
from src.catalogo_curso import CatalogoCurso
from src.aluno import Aluno
from src.curso import Curso
from src.coordenador_curso import CoordenadorCurso
from src.materia import Materia
from src.banco_dados import BancoDados

class TestCoordenador:
    coordenador = None
    bd = None

    def setup_method(self, method):
        self.bd = BancoDados(sqlite3.connect(":memory:"))
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
        self.bd.fecha_conexao_existente()
        
    
    def test_coordenador_curso_2_nao_pode_listar_alunos_curso_1(self):
        expected = {"alunos":[]}
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
        expected = {"alunos":[
            {
                "nome": nome_1,
                "materias": materias_1,
                "coeficiente rendimento": cr_1
            },
            {
                "nome": nome_2,
                "materias": materias_2,
                "coeficiente rendimento": cr_2
            },
            ]
        }
        self._cria_aluno_no_curso(nome_1, self.curso, materias_1)
        self._cria_aluno_no_curso(nome_2, self.curso, materias_2)
        actual = self.coordenador.listar_detalhe_alunos()
        assert actual == expected 

    def test_coordenador_curso_pode_listar_alunos_do_curso_com_um_aluno(self):
        nome = "marcos"
        materias = {"civil":5}
        cr = 5
        expected = {"alunos": [{"nome": nome, "materias": materias, "coeficiente rendimento": cr}]}       
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
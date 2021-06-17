from src.model.materia import Materia
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.controller.controller import Controller
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.model.coordenador_geral import CoordenadorGeral
from tests.massa_dados import aluno_nome_1, curso_nome_1, materia_nome_1
from src.model.associa_curso_materia import AssociaCursoMateria


class TestControllerCoordenadorGeral:

    def test_popula_banco(self, cria_banco, cria_massa_dados_em_memoria):
        expected = {
                        "alunos": [
                            {
                                "nome": aluno_nome_1,
                                "coeficiente rendimento": 0,
                                "materias": {}
                            }
                        ]
                    }
        coordenador_geral = self._setup_objetos(cria_banco)
        actual = coordenador_geral.listar_detalhe_alunos()
        assert actual == expected

    def _setup_objetos(self, cria_banco):
        controller_aluno = Controller(Aluno(aluno_nome_1), cria_banco)
        controller_aluno.salva()
        aluno = controller_aluno.pega_registro_por_id(id=1)
        controller_curso = Controller(Curso(curso_nome_1), cria_banco)
        controller_curso.salva()
        curso = controller_curso.pega_registro_por_id(id=1)
        Controller(InscricaoAlunoCurso(aluno_id=1,
                                       curso_id=1),
                   cria_banco).salva()
        controller_materia = Controller(Materia(materia_nome_1), cria_banco)
        controller_materia.salva()
        materia_1 = controller_materia.pega_registro_por_id(id=1)
        controller_materia = Controller(Materia(materia_nome_1), cria_banco)
        controller_materia.salva()
        materia_2 = controller_materia.pega_registro_por_id(id=2)
        controller_materia = Controller(Materia(materia_nome_1), cria_banco)
        controller_materia.salva()
        materia_3 = controller_materia.pega_registro_por_id(id=3)
        Controller(AssociaCursoMateria(curso_id=1,
                                       materia_id=1), cria_banco).salva()
        Controller(AssociaCursoMateria(curso_id=1,
                                       materia_id=2), cria_banco).salva()
        Controller(AssociaCursoMateria(curso_id=1,
                                       materia_id=3), cria_banco).salva()
        controller_coordenador_geral = Controller(CoordenadorGeral(),
                                                  cria_banco)
        controller_coordenador_geral.salva()
        coordenador_geral = controller_coordenador_geral \
            .pega_registro_por_id(id=1)
        curso.atualiza_materias(materia_1)
        curso.atualiza_materias(materia_2)
        curso.atualiza_materias(materia_3)
        aluno.inscreve_curso(curso)
        return coordenador_geral

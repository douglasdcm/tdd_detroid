from src.model.materia import Materia
from src.model.inscricao_aluno_curso import InscricaoAlunoCurso
from src.controller.controller import Controller
from src.model.aluno import Aluno
from src.model.curso import Curso
from src.model.coordenador_geral import CoordenadorGeral
from tests.massa_dados import aluno_nome_1, curso_nome_1, materia_nome_1, materia_nome_2, materia_nome_3
from src.model.associa_curso_materia import AssociaCursoMateria


class TestControllerCoordenadorGeral:

    def test_popula_banco(self, cria_banco, cria_massa_dados_em_memoria):
        expected = {
                        "alunos": [
                            {
                                "nome": aluno_nome_1,
                                "coeficiente rendimento": 0,
                                "materias": {},
                                "curso": curso_nome_1
                            }
                        ]
                    }
        coordenador_geral = self._setup_objetos(cria_banco)
        actual = coordenador_geral.listar_detalhe_alunos()
        assert actual == expected

    def _setup_objetos(self, cria_banco):
        controller_aluno = Controller(Aluno(aluno_nome_1), cria_banco)
        controller_aluno.salva()
        aluno_obj = controller_aluno.pega_registro_por_id(id_=1)
        controller_curso = Controller(Curso(curso_nome_1), cria_banco)
        controller_curso.salva()
        curso_obj = controller_curso.pega_registro_por_id(id_=1)
        controller_materia = Controller(Materia(materia_nome_1), cria_banco)
        controller_materia.salva()
        materia_1_obj = controller_materia.pega_registro_por_id(id_=1)
        controller_materia = Controller(Materia(materia_nome_2), cria_banco)
        controller_materia.salva()
        materia_2_obj = controller_materia.pega_registro_por_id(id_=2)
        controller_materia = Controller(Materia(materia_nome_3), cria_banco)
        controller_materia.salva()
        materia_3_obj = controller_materia.pega_registro_por_id(id_=3)
        curso_obj = curso_obj.atualiza_materias(materia_1_obj)
        curso_obj = curso_obj.atualiza_materias(materia_2_obj)
        curso_obj = curso_obj.atualiza_materias(materia_3_obj)
        aluno_obj = aluno_obj.inscreve_curso(curso_obj)
        Controller(AssociaCursoMateria(curso_obj,
                                       materia_1_obj), cria_banco).salva()
        Controller(AssociaCursoMateria(curso_obj,
                                       materia_2_obj), cria_banco).salva()
        Controller(AssociaCursoMateria(curso_obj,
                                       materia_3_obj), cria_banco).salva()
        Controller(InscricaoAlunoCurso(aluno_obj,
                                       curso_obj),
                   cria_banco).salva()
        controller_coordenador_geral = Controller(CoordenadorGeral(),
                                                  cria_banco)
        controller_coordenador_geral.salva()
        coordenador_geral = controller_coordenador_geral \
            .pega_registro_por_id(id_=1)
        return coordenador_geral

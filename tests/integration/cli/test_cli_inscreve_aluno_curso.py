from src.model.curso import Curso
from tests.helper import executa_comando
from tests.massa_dados import aluno_nome_1, curso_nome_1

class TestCliInscreveAlunoCurso:   

    def test_aluno_pode_ser_inscrito_curso(self, cria_massa_dados):
        aluno_id = "1"
        curso_id = "1"
        expected = f"Aluno {aluno_nome_1} inscrito no curso de {curso_nome_1}."
        parametros = ["inscreve-aluno-curso", "--aluno-id", aluno_id, "--curso-id",
                curso_id]
        actual = executa_comando(parametros)
        assert actual == expected

    # def test_aluno_inscrito_curso_salvo_banco_dados(self, cria_banco, \
    #         cria_aluno, cria_curso_com_materias):
    #     aluno_id = "1"
    #     curso_id = "1"
    #     aluno = cria_aluno
    #     curso = cria_curso_com_materias
    #     expected = [tuple((aluno_id,curso_id))]
    #     parametros = ["inscreve-aluno-curso", "--aluno-id", aluno_id, "--curso-id",
    #             curso_id]
    #     executa_comando(parametros)
    #     inscricao = InscricaoAlunoCurso(aluno, curso)
    #     actual = DaoFabrica(inscricao, cria_banco) \
    #                 .fabrica_objetos_dao() \
    #                 .pega_tudo()
    #     assert actual == expected
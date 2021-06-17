from src.dao.dao_curso import DaoCurso
from src.model.curso import Curso
from tests.massa_dados import curso_nome_1

class TestDaoCurso:

    def _setup_curso(self, cria_banco, id=None, nome=None):
        expected = Curso(nome)
        expected.define_id(id)
        dao = DaoCurso(Curso(nome), cria_banco)
        dao.salva()
        return expected, dao

    def _pega_todos_registros(self, cria_banco, id=None, nome=None):
        expected, dao = self._setup_curso(cria_banco, id, nome)
        actual = dao.pega_tudo()
        return expected, actual

    def _pega_registro_por_id(self, cria_banco, id=None, nome=None):
        expected, dao = self._setup_curso(cria_banco, id, nome)
        actual = dao.pega_por_id(id)
        return expected, actual

    def test_curso_recupera_nome_por_id(self, cria_banco):
        expected, actual = self._pega_registro_por_id(cria_banco, id=1, 
                                nome=curso_nome_1)
        assert actual.pega_nome() == expected.pega_nome()

    def test_curso_recupera_id_banco_por_id(self, cria_banco):
        expected, actual = self._pega_registro_por_id(cria_banco, id=1, 
                                nome=curso_nome_1)
        assert actual.pega_id() == expected.pega_id()

    def test_multiplos_cursos_recuperados_banco_dados(self, cria_banco):
        indice = 2
        self._setup_curso(cria_banco)
        self._setup_curso(cria_banco)
        expected, actual = self._pega_todos_registros(cria_banco, id=3, 
                                    nome=curso_nome_1)
        assert actual[indice].pega_id() == expected.pega_id()

    def test_nome_curso_recuperado_banco_dados(self, cria_banco):
        expected, actual = self._pega_todos_registros(cria_banco, id=1, 
                                nome=curso_nome_1)
        assert actual[0].pega_nome() == expected.pega_nome()

    def test_curso_id_recuperado_do_banco_dados(self, cria_banco):
        expected, actual = self._pega_todos_registros(cria_banco, id=1, 
                                    nome=curso_nome_1)
        assert actual[0].pega_id() == expected.pega_id()

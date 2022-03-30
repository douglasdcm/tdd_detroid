from src.model.materia import Materia


class TestMateria:
    def test_os_nomes_das_materias_nao_precisam_ser_diferentes(self):
        expected = "matematica"
        materia_1 = Materia(expected)
        materia_2 = Materia(expected)
        actual_1 = materia_1.pega_nome()
        actual_2 = materia_2.pega_nome()
        assert actual_1 == actual_2

    def test_cada_materia_deve_ter_um_nome(self):
        expected = "matematica"
        materia = Materia(expected)
        actual = materia.pega_nome()
        assert actual == expected

    def test_materias_curso_devem_ter_identificadores_unicos(self):
        expected = "1"
        materia = Materia("mat")
        materia.define_id(expected)
        actual = materia.pega_id()
        assert actual == expected

from src.model.coordenador_geral import CoordenadorGeral
from src.model.materia import Materia
from src.model.curso import Curso
from src.model.aluno import Aluno
from src.model.catalogo_curso import CatalogoCurso


class TestCenarioTresAlunosCincoCursos:

    def test_faculdade_com_dois_alunos_aprovados_e_um_reprovado_no_curso(self):
        '''
        Faculdade de exatas. Tem 3 alunos e 5 cursos. Dois alunos fazem matérias iguais e um não faz
        nenhuma matéria com os demais.
        '''
        CatalogoCurso.limpa_catalogo()
        pedro = Aluno("Pedro")
        jose = Aluno("Jose")
        tiago = Aluno("Tiago")
        coordenador_geral = CoordenadorGeral()

        fisica = Curso("Fisica")
        fisica.atualiza_materias(Materia("Ótica"))
        fisica.atualiza_materias(Materia("Mecânica"))
        fisica.atualiza_materias(Materia("Elátrica"))
        coordenador_fisica = CoordenadorGeral(fisica)

        matematica = Curso("Matematica")
        matematica.atualiza_materias(Materia("Geometria"))
        matematica.atualiza_materias(Materia("Cálculo"))
        matematica.atualiza_materias(Materia("Algebra"))
        coordenador_matematica = CoordenadorGeral(matematica)

        informatica = Curso("Informatica")
        informatica.atualiza_materias(Materia("Programação"))
        informatica.atualiza_materias(Materia("Dados"))
        informatica.atualiza_materias(Materia("Hardware"))
        coordenador_informatica = CoordenadorGeral(informatica)

        engenharia_civil = Curso("Engenharia Civil")
        engenharia_civil.atualiza_materias(Materia("Estrutura"))
        engenharia_civil.atualiza_materias(Materia("Concreto armado"))
        engenharia_civil.atualiza_materias(Materia("Hidráulica"))
        coordenador_engenharia_civil = CoordenadorGeral(engenharia_civil)

        eletronica = Curso("Eletrônica")
        eletronica.atualiza_materias(Materia("Robótica"))
        eletronica.atualiza_materias(Materia("Chips"))
        eletronica.atualiza_materias(Materia("Circuitos"))
        coordenador_eletronica = CoordenadorGeral(eletronica)

        pedro.inscreve_curso(eletronica)
        jose.inscreve_curso(eletronica)
        tiago.inscreve_curso(engenharia_civil)

        print("\nPrimeiro semestre")
        pedro.atualiza_materias_cursadas({"Robótica": 10})
        jose.atualiza_materias_cursadas({"Robótica": 6})
        tiago.atualiza_materias_cursadas({"Concreto armado": 8})

        print("\nRelatório geral")
        print(coordenador_geral.listar_detalhe_alunos())
        print("\nRelatório dos cursos")
        print(coordenador_eletronica.listar_detalhe_alunos())
        print(coordenador_engenharia_civil.listar_detalhe_alunos())
        print(coordenador_fisica.listar_detalhe_alunos())
        print(coordenador_informatica.listar_detalhe_alunos())
        print(coordenador_matematica.listar_detalhe_alunos())

        print("\nSegundo semestre")
        pedro.atualiza_materias_cursadas({"Chips": 9})
        jose.atualiza_materias_cursadas({"Robótica": 9})
        tiago.atualiza_materias_cursadas({"Estrutura": 0})

        print("\nRelatório geral")
        print(coordenador_geral.listar_detalhe_alunos())
        print("\nRelatório dos cursos")
        print(coordenador_eletronica.listar_detalhe_alunos())
        print(coordenador_engenharia_civil.listar_detalhe_alunos())
        print(coordenador_fisica.listar_detalhe_alunos())
        print(coordenador_informatica.listar_detalhe_alunos())
        print(coordenador_matematica.listar_detalhe_alunos())

        print("\nTerceiro semestre")
        pedro.atualiza_materias_cursadas({"Circuitos": 7})
        jose.atualiza_materias_cursadas({"Chips": 9})
        tiago.atualiza_materias_cursadas({"Estrutura": 10})

        print("\nRelatório geral")
        print(coordenador_geral.listar_detalhe_alunos())
        print("\nRelatório dos cursos")
        print(coordenador_eletronica.listar_detalhe_alunos())
        print(coordenador_engenharia_civil.listar_detalhe_alunos())
        print(coordenador_fisica.listar_detalhe_alunos())
        print(coordenador_informatica.listar_detalhe_alunos())
        print(coordenador_matematica.listar_detalhe_alunos())
        pedro.calcula_situacao()
        jose.calcula_situacao()
        tiago.calcula_situacao()
        print(pedro.pega_situacao())
        print(jose.pega_situacao())
        print(tiago.pega_situacao())

        print("\nQuarto semestre")
        jose.atualiza_materias_cursadas({"Circuitos": 9.7})
        tiago.atualiza_materias_cursadas({"Hidráulica": 3})

        print("\nRelatório geral")
        print(coordenador_geral.listar_detalhe_alunos())
        print("\nRelatório dos cursos")
        print(coordenador_eletronica.listar_detalhe_alunos())
        print(coordenador_engenharia_civil.listar_detalhe_alunos())
        print(coordenador_fisica.listar_detalhe_alunos())
        print(coordenador_informatica.listar_detalhe_alunos())
        print(coordenador_matematica.listar_detalhe_alunos())
        pedro.calcula_situacao()
        jose.calcula_situacao()
        tiago.calcula_situacao()
        print(pedro.pega_situacao())
        print(jose.pega_situacao())
        print(tiago.pega_situacao())

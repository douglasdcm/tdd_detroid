from tests.helper import executa_comando

class TestCliCurso:

    def test_criacao_de_curso_com_menos_materias_que_o_minimo_retorna_excecao(self):
        expected = "Lista de parâmetros inválida."
        comando = ["python", "main.py", "cria-curso", "--nome", "Matemática", 
                    "-m", "algebra", "calculo"]
        actual = executa_comando(comando)
        assert expected in actual

    def test_criacao_de_curso_sem_materias_retorna_excecao(self):
        expected = "Lista de parâmetros inválida."
        comando = ["python", "main.py", "cria-curso", "--nome", "Matemática", "-m"]
        actual = executa_comando(comando)
        assert expected in actual

    def test_criacao_de_curso_sem_nome_retorna_excecao(self):
        expected = "Lista de parâmetros inválida."
        comando = ["python", "main.py", "cria-curso", "--nome", "-m",
                     "algebra", "cálculo", "lógica"]
        actual = executa_comando(comando)
        assert expected in actual

    def test_criacao_de_curso_usando_tag__m__para_lista_das_materias(self):
        expected = "Curso de Matemática criado."
        comando = ["python", "main.py", "cria-curso", "--nome", "Matemática", "-m",
                     "algebra", "cálculo", "lógica"]
        actual = executa_comando(comando)
        assert actual == expected

    def test_criacao_de_curso_usando_tag__n__para_nome_do_curso(self):
        expected = "Curso de Matemática criado."
        comando = ["python", "main.py", "cria-curso", "-n", "Matemática", "--materias",
                     "algebra", "cálculo", "lógica"]
        actual = executa_comando(comando)
        assert actual == expected

    def test_criacao_de_curso_com_numero_minimo_de_materias(self):
        expected = "Curso de Matemática criado."
        comando = ["python", "main.py", "cria-curso", "--nome", "Matemática", "--materias",
                     "algebra", "cálculo", "lógica"]
        actual = executa_comando(comando)
        assert actual == expected
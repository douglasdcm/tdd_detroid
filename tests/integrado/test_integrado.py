from src.modelos.curso import ErroCurso
from src.cursos import Cursos
from src.materias import Materias
from src.alunos import Alunos
from src.esquemas.curso import CursoBd
from src.esquemas.materia import MateriaBd
from src.utils.utils import inicializa_tabelas
from src.utils.exceptions import ErroAluno, ErroMateria
from tests.config import conn
from tests.utils import cria_curso, cria_materia
from pytest import raises
from time import sleep


def test_cria_aluno_por_api():
    alunos = Alunos(conn)
    alunos.cria("any")
    aluno = alunos.lista(1)
    assert aluno.id == 1


def test_cli_tres_cursos_com_tres_materias_cada():
    cursos = Cursos(conn)
    materias = Materias(conn)
    cria_curso(conn)
    cria_curso(conn)
    cria_curso(conn)
    for _ in range(3):
        cria_materia(conn, 1)
        cria_materia(conn, 2)
        cria_materia(conn, 3)

    # verifica pela API
    assert len(cursos.lista_tudo()) == 3
    assert len(materias.lista_tudo()) == 9


def test_aluno_pode_se_inscrever_em_apenas_um_curso(popula_banco_dados):
    alunos = Alunos(conn)
    alunos.cria("any")
    Cursos(conn).cria("other")
    alunos.inscreve_curso(1, 4)

    for _ in range(3):
        if alunos.lista(1).curso_id is not None:
            break
        sleep(1)

    with raises(ErroAluno, match="Aluno esta inscrito em outro curso"):
        alunos.inscreve_curso(1, 3)

    aluno = alunos.lista(1)
    assert aluno.curso_id == 4


def test_curso_nao_pode_ter_materias_com_mesmo_nome():

    Cursos(conn).cria("any_1")
    Cursos(conn).cria("any_2")
    Cursos(conn).cria("any_3")
    Materias(conn).cria("any", 1)
    with raises(
        ErroMateria,
        match="O curso já possui uma matéria com este nome",
    ):
        Materias(conn).cria("any", 1)


def test_nao_criar_quarto_curso_se_menos_de_tres_materias_por_curso():
    Cursos(conn).cria("any_1")
    Cursos(conn).cria("any_2")
    Cursos(conn).cria("any_3")
    Materias(conn).cria(nome="any", curso_id=1)
    with raises(
        ErroCurso,
        match="Necessários 3 cursos com 3 três matérias para se criar novos cursos",
    ):
        Cursos(conn).cria("quarto")


def test_nao_criar_quarto_curso_se_todos_cursos_sem_materias():
    Cursos(conn).cria("any_1")
    Cursos(conn).cria("any_2")
    Cursos(conn).cria("any_3")
    with raises(
        ErroCurso,
        match="Necessários 3 cursos com 3 três matérias para se criar novos cursos",
    ):
        Cursos(conn).cria("quatro")


def test_materia_nao_criada_se_menos_de_tres_cursos_existentes():
    with raises(
        ErroMateria, match="Necessários 3 cursos para se criar a primeira matéria"
    ):
        Materias(conn).cria("any", 1)


def test_materia_nao_associada_curso_inexistente(popula_banco_dados):
    with raises(ErroMateria):
        Materias(conn).cria("any", 42)


def test_materia_associada_curso_existente():
    conn.cria(CursoBd(nome="any"))
    conn.cria(MateriaBd(nome="any", curso=1))
    assert conn.lista(MateriaBd, 1).nome == "any"


def test_cria_tabela_com_dados():
    conn.cria(CursoBd(nome="any_1"))
    conn.cria(CursoBd(nome="any_2"))
    conn.cria(CursoBd(nome="any_3"))
    assert len(conn.lista_tudo(CursoBd)) == 3


def test_cria_item_bd():
    conn.cria(CursoBd(nome="any"))
    assert len(conn.lista_tudo(CursoBd)) == 1


def test_lista_por_id_bd():
    Cursos(conn).cria("any")
    inicializa_tabelas(conn)
    assert len(conn.lista_tudo(CursoBd)) == 0

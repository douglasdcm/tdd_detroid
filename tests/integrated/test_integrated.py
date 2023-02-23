from src.sdk import courses
from src.disciplines import Disciplines
from src.sdk.students import Students
from src.schemes.student import StudentDB
from src.schemes.course import CourseDB
from src.schemes.discipline import MateriaBd
from src.schemes.for_association import MateriaStudentDB
from src.utils.utils import inicializa_tabelas
from src.utils.exceptions import (
    ErroAluno,
    ErroMateria,
    ErrorCourse,
    ErroMateriaAluno,
)
from tests.config import conn
from tests.utils import cria_curso, cria_materia
from pytest import raises


def test_calcula_cr_aluno_de_materias_cursadas(popula_banco_dados):
    aluno_id = len(Students(conn).lista_tudo())
    alunos = Students(conn)
    alunos.set_grade(aluno_id=aluno_id, materia_id=1, nota=5)
    alunos.set_grade(aluno_id=aluno_id, materia_id=2, nota=0)
    alunos.set_grade(aluno_id=aluno_id, materia_id=3, nota=5)

    assert conn.get(StudentDB, aluno_id).coef_rend == 5


def test_alunos_deve_inscreve_em_3_materias(popula_banco_dados):

    alunos = Students(conn)
    alunos.create("any")
    aluno_id = len(alunos.lista_tudo())
    alunos.subscribe_in_course(aluno_id, curso_id=1)
    with raises(
        ErroMateriaAluno, match="Aluno deve se inscrever em 3 materias no minimo"
    ):
        alunos.subscribe_in_discipline(aluno_id, 1)

    materia_aluno = conn.lista_tudo(MateriaStudentDB)
    assert len(materia_aluno) > 1


def test_cria_aluno_por_api():
    alunos = Students(conn)
    alunos.create("any")
    aluno = alunos.lista(1)
    assert aluno.id == 1


def test_cli_tres_cursos_com_tres_materias_cada():
    materias = Disciplines(conn)
    cria_curso(conn)
    cria_curso(conn)
    cria_curso(conn)
    for _ in range(3):
        cria_materia(conn, 1)
        cria_materia(conn, 2)
        cria_materia(conn, 3)

    # verifica pela API
    assert len(courses.get_all()) == 3
    assert len(materias.lista_tudo()) == 9


def test_aluno_pode_se_inscrever_em_apenas_um_curso(popula_banco_dados):
    alunos = Students(conn)
    alunos.create("any")
    aluno_id = len(alunos.lista_tudo())
    courses.create("other")
    alunos.subscribe_in_course(aluno_id, 4)

    with raises(ErroAluno, match="Aluno esta inscrito em outro curso"):
        alunos.subscribe_in_course(aluno_id, 3)

    aluno = alunos.lista(aluno_id)
    assert aluno.curso_id == 4


def test_curso_nao_pode_ter_materias_com_mesmo_nome():

    courses.create("any_1")
    courses.create("any_2")
    courses.create("any_3")
    Disciplines(conn).cria("any", 1)
    with raises(
        ErroMateria,
        match="O curso já possui uma matéria com este nome",
    ):
        Disciplines(conn).cria("any", 1)


def test_nao_criar_quarto_curso_se_menos_de_tres_materias_por_curso():
    courses.create("any_1")
    courses.create("any_2")
    courses.create("any_3")
    Disciplines(conn).cria(nome="any", curso_id=1)
    with raises(
        ErrorCourse,
        match="Necessários 3 cursos com 3 três matérias para se criar novos cursos",
    ):
        courses.create("quarto")


def test_nao_criar_quarto_curso_se_todos_cursos_sem_materias():
    courses.create("any_1")
    courses.create("any_2")
    courses.create("any_3")
    with raises(
        ErrorCourse,
        match="Necessários 3 cursos com 3 três matérias para se criar novos cursos",
    ):
        courses.create("quatro")


def test_materia_nao_criada_se_menos_de_tres_cursos_existentes():
    with raises(
        ErroMateria, match="Necessários 3 cursos para se criar a primeira matéria"
    ):
        Disciplines(conn).cria("any", 1)


def test_materia_nao_associada_curso_inexistente(popula_banco_dados):
    with raises(ErroMateria):
        Disciplines(conn).cria("any", 42)


def test_materia_associada_curso_existente():
    conn.cria(CourseDB(nome="any"))
    conn.cria(MateriaBd(nome="any", curso_id=1))
    assert conn.get(MateriaBd, 1).nome == "any"


def test_cria_tabela_com_dados():
    conn.cria(CourseDB(nome="any_1"))
    conn.cria(CourseDB(nome="any_2"))
    conn.cria(CourseDB(nome="any_3"))
    assert len(conn.lista_tudo(CourseDB)) == 3


def test_cria_item_bd():
    conn.cria(CourseDB(nome="any"))
    assert len(conn.lista_tudo(CourseDB)) == 1


def test_lista_por_id_bd():
    courses.create("any")
    inicializa_tabelas(conn)
    assert len(conn.lista_tudo(CourseDB)) == 0

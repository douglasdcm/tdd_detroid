from src.controllers import courses
from src.controllers import disciplines
from src.controllers import students
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
from src.utils import sql_client
from tests.utils import create_curso, create_materia
from pytest import raises


def test_calcula_cr_aluno_de_materias_cursadas(popula_banco_dados):
    student_id = len(students.get_all())

    students.set_grade(student_id=student_id, discipline_id=1, grade=5)
    students.set_grade(student_id=student_id, discipline_id=2, grade=0)
    students.set_grade(student_id=student_id, discipline_id=3, grade=5)

    assert sql_client.get(StudentDB, student_id).coef_rend == 5


def test_students_deve_inscreve_em_3_materias(popula_banco_dados):

    students.create("any")
    student_id = len(students.get_all())
    students.subscribe_in_course(student_id, curso_id=1)
    with raises(
        ErroMateriaAluno, match="Aluno deve se inscrever em 3 materias no minimo"
    ):
        students.subscribe_in_discipline(student_id, 1)

    materia_aluno = sql_client.get_all(MateriaStudentDB)
    assert len(materia_aluno) > 1


def test_create_aluno_por_api():

    students.create("any")
    aluno = students.get(1)
    assert aluno.id == 1


def test_cli_tres_cursos_com_tres_materias_cada():
    create_curso()
    create_curso()
    create_curso()
    for _ in range(3):
        create_materia(1)
        create_materia(2)
        create_materia(3)

    # verifica pela API
    assert len(courses.get_all()) == 3
    assert len(disciplines.get_all()) == 9


def test_aluno_pode_se_inscrever_em_apenas_um_curso(popula_banco_dados):

    students.create("any")
    student_id = len(students.get_all())
    courses.create("other")
    students.subscribe_in_course(student_id, 4)

    with raises(ErroAluno, match="Aluno esta inscrito em outro curso"):
        students.subscribe_in_course(student_id, 3)

    aluno = students.get(student_id)
    assert aluno.curso_id == 4


def test_curso_nao_pode_ter_materias_com_mesmo_nome():

    courses.create("any_1")
    courses.create("any_2")
    courses.create("any_3")
    disciplines.create("any", 1)
    with raises(
        ErroMateria,
        match="O curso já possui uma matéria com este nome",
    ):
        disciplines.create("any", 1)


def test_nao_criar_quarto_curso_se_menos_de_tres_materias_por_curso():
    courses.create("any_1")
    courses.create("any_2")
    courses.create("any_3")
    disciplines.create(nome="any", curso_id=1)
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


def test_materia_nao_createda_se_menos_de_tres_cursos_existentes():
    with raises(
        ErroMateria, match="Necessários 3 cursos para se criar a primeira matéria"
    ):
        disciplines.create("any", 1)


def test_materia_nao_associada_curso_inexistente(popula_banco_dados):
    with raises(ErroMateria):
        disciplines.create("any", 42)


def test_materia_associada_curso_existente():
    sql_client.create(CourseDB(nome="any"))
    sql_client.create(MateriaBd(nome="any", curso_id=1))
    assert sql_client.get(MateriaBd, 1).nome == "any"


def test_create_tabela_com_dados():
    sql_client.create(CourseDB(nome="any_1"))
    sql_client.create(CourseDB(nome="any_2"))
    sql_client.create(CourseDB(nome="any_3"))
    assert len(sql_client.get_all(CourseDB)) == 3


def test_create_item_bd():
    sql_client.create(CourseDB(nome="any"))
    assert len(sql_client.get_all(CourseDB)) == 1


def test_lista_por_id_bd():
    courses.create("any")
    inicializa_tabelas()
    assert len(sql_client.get_all(CourseDB)) == 0

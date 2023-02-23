from src.schemes.for_association import MateriaStudentDB
from src.schemes.student import StudentDB
from src.controllers import students
from src.utils.exceptions import (
    ErroAluno,
    ErroMateriaAluno,
    ErroMateria,
    ErrorCourse,
)
from tests.config import conn
from pytest import raises, mark


@mark.parametrize("input", [(""), ("   ")])
def test_student_name_cannot_be_empty(popula_banco_dados, input):
    with raises(ErroAluno, match="Invalid student name"):
        students.create(nome=input)


def test_arredonda_o_cr_a_uma_casa_decimal(popula_banco_dados):
    student_id = len(conn.get_all(StudentDB))
    students.id = student_id
    students.set_grade(student_id, discipline_id=1, grade=2)
    students.set_grade(student_id, discipline_id=2, grade=2)
    students.set_grade(student_id, discipline_id=3, grade=3)
    aluno_bd = conn.get(StudentDB, student_id)
    assert aluno_bd.coef_rend == 2.3


def test_calcula_cr_aluno_como_media_simples_das_notas_lancadas(popula_banco_dados):
    student_id = len(conn.get_all(StudentDB))
    students.set_grade(student_id, discipline_id=1, grade=1)
    students.set_grade(student_id, discipline_id=2, grade=2)
    students.set_grade(student_id, discipline_id=3, grade=3)
    aluno_bd = conn.get(StudentDB, student_id)
    assert aluno_bd.coef_rend == 2


def test_lanca_nota_se_aluno_existe(popula_banco_dados):
    controller = students
    student_id = len(controller.get_all())

    controller.id = student_id
    materia_id = 1
    nota = 7
    assert controller.set_grade(student_id, materia_id, nota) is None


def test_assume_maior_nota_se_duplo_lancamento_de_notas(popula_banco_dados):
    controller = students
    student_id = len(controller.get_all())

    controller.id = student_id
    materia_id = 1
    nota = 7
    nota_bd = None
    controller.set_grade(student_id, materia_id, grade=nota + 1)
    controller.set_grade(student_id, materia_id, grade=nota)
    mas = conn.get_all(MateriaStudentDB)
    for ma in mas:
        if ma.student_id == student_id and ma.materia_id == materia_id:
            nota_bd = ma.aluno_nota
            break
    assert nota == nota_bd


def test_nao_lanca_nota_se_menor_que_zero():
    controller = students
    student_id = len(controller.get_all())
    controller.create("any")
    materia_id = 1
    with raises(ErroAluno, match="Nota não pode ser menor que 0"):
        controller.set_grade(student_id, materia_id, grade=-1)


def test_nao_lanca_nota_se_maoir_que_10():
    controller = students
    student_id = len(controller.get_all())

    controller.create("any")
    materia_id = 1
    with raises(ErroAluno, match="Nota não pode ser maior que 10"):
        controller.set_grade(student_id, materia_id, grade=11)


def test_nao_lanca_nota_se_aluno_nao_inscrito_materia():
    controller = students
    student_id = len(controller.get_all())

    controller.create("any")
    materia_id = 1
    with raises(
        ErroAluno, match=f"Aluno {student_id} não está inscrito na matéria {materia_id}"
    ):
        controller.set_grade(student_id, materia_id, grade=5)


def test_lanca_notas_se_aluno_inscrito_materia(popula_banco_dados):
    controller = students
    student_id = len(controller.get_all())

    controller.id = student_id
    controller.set_grade(student_id, discipline_id=1, grade=5)
    assert conn.get(StudentDB, student_id).coef_rend == 5.0


def test_nao_inscreeve_aluno_se_curso_nao_existe():
    controller = students
    controller.create("any")
    student_id = len(controller.get_all())
    with raises(ErroAluno, match="Aluno 1 não está inscrito em nenhum curso"):
        controller.subscribe_in_discipline(student_id, 1)


def test_mensagem_sobre_3_materias_para_apos_inscricao_em_3_materias(
    popula_banco_dados,
):

    controller = students
    controller.create("any")
    student_id = len(controller.get_all())
    controller.subscribe_in_course(student_id, curso_id=1)
    with raises(ErroMateriaAluno):
        controller.subscribe_in_discipline(student_id, 1)
    with raises(ErroMateriaAluno):
        controller.subscribe_in_discipline(student_id, 2)
    controller.subscribe_in_discipline(student_id, 3)


def test_aluno_nao_pode_se_inscrever_em_materia_inexistente(popula_banco_dados):
    student_id = len(conn.get_all(StudentDB))
    students.id = student_id
    with raises(ErroMateriaAluno):
        students.subscribe_in_discipline(student_id, 1)
        students.subscribe_in_discipline(student_id, 2)
        students.subscribe_in_discipline(student_id, 3)
    with raises(ErroMateria, match="Matéria 42 não existe"):
        students.subscribe_in_discipline(student_id, 42)


def test_aluno_nao_pode_se_inscrever_duas_vezes_na_mesma_materia(popula_banco_dados):
    student_id = len(conn.get_all(StudentDB))
    controller = students
    controller.id = student_id
    with raises(ErroMateriaAluno):
        controller.subscribe_in_discipline(student_id, 1)
        controller.subscribe_in_discipline(student_id, 2)
        controller.subscribe_in_discipline(student_id, 3)
    with raises(ErroMateriaAluno, match="Aluno 1 já está inscrito na matéria 1"):
        controller.subscribe_in_discipline(student_id, 1)


def test_inscreve_aluno_numa_materia(popula_banco_dados):
    controller = students
    controller.create("any")
    student_id = len(controller.get_all())
    controller.subscribe_in_course(student_id, curso_id=1)
    with raises(
        ErroMateriaAluno, match="Aluno deve se inscrever em 3 materias no minimo"
    ):
        controller.subscribe_in_discipline(student_id, 1)


def test_aluno_create():
    students.create(nome="any")
    assert conn.get(StudentDB, 1).nome == "any"
    assert conn.get(StudentDB, 1).id == 1


def test_inscreve_aluno_se_curso_existe():
    students.create("any")
    with raises(Exception):
        with raises(ErrorCourse, match="Curso 42 nao existe"):
            students.subscribe_in_course(curso_id=42)


def test_inscreve_aluno_curso(popula_banco_dados):
    controller = students
    controller.create("any")
    student_id = len(controller.get_all())
    controller.subscribe_in_course(student_id, curso_id=1)
    assert conn.get(StudentDB, 1).curso_id == 1


def test_verifica_aluno_existe():
    with raises(ErroAluno, match="Aluno 42 não existe"):
        students.id = 42


def test_nao_inscreve_aluno_se_curso_nao_existe():
    controller = students
    controller.create("any")
    student_id = len(controller.get_all())
    with raises(ErroAluno, match="Curso 42 não existe"):
        controller.subscribe_in_course(student_id, 42)


def test_alunos_lista_por_id():
    students.create(nome="any")
    students.create(nome="other")
    assert conn.get(StudentDB, id_=2).nome == "other"


def test_alunos_get_all():
    students.create(nome="any")
    students.create(nome="other")
    assert len(conn.get_all(StudentDB)) == 2


def test_alunos_create_banco_dados():
    students.create(nome="any")
    assert conn.get(StudentDB, id_=1).nome == "any"
